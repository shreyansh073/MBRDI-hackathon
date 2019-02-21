import glob
import os
import sys
import json
from plyfile import PlyData, PlyElement
import numpy as np

try:
    sys.path.append(glob.glob('**/*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time

### Callback function to save the generated point cloud into .ply and single .json file format
def callback(lidar_measurement,objects):

    filename = '_out/%06d.ply' % lidar_measurement.frame_number
    lidar_measurement.save_to_disk(filename)        # Save .ply file

    plydata = PlyData.read(filename)

    x = plydata['vertex']['x']
    y = plydata['vertex']['y']
    z = plydata['vertex']['z']

    x = np.float64(x)
    y = np.float64(y)
    z = np.float64(z)

    cloud = []
    for i in range(plydata.elements[0].count):
        points = {
            "Pos_x": x[i],
            "Pos_y": -y[i],
            "Pos_z": z[i],
        }
        cloud.append(points)
    pos = {
        "Pos_X": 13.375,
        "Pos_Y": 20
    }
    obj=dict(VehiclePostion=[pos],Lidar=cloud)
    objects.append(obj)


def main(callback=None):
    actor_list = []
    objects = []

    try:

        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        bp = random.choice(blueprint_library.filter('vehicle'))

        transform = carla.Transform(carla.Location(x=13.75, y=-20, z=0), carla.Rotation(yaw=-90))
        vehicle = world.spawn_actor(bp, transform)
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)

        vehicle.set_autopilot(True)

        #Attach Lidar onto the vehicle
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('range', '5000')
        lidar_bp.set_attribute('channels', '64')
        lidar_bp.set_attribute('points_per_second', '100000')
        #lidar_bp.set_attribute('rotation_frequency', '0')
        lidar_bp.set_attribute('upper_fov', '15.0')
        lidar_bp.set_attribute('lower_fov', '-25.0')

        lidar_transform = carla.Transform(carla.Location(z=3))
        lidar = world.spawn_actor(lidar_bp,lidar_transform,attach_to = vehicle)
        #print(lidar.transform)
        actor_list.append(lidar)
        print('created %s' % lidar.type_id)

        #Save generated point clouds
        lidar_measurement = carla.LidarMeasurement
        lidar.listen(lambda lidar_measurement: callback(lidar_measurement,objects))

        ### Attach Depth camera
        camera_bp = blueprint_library.find('sensor.camera.depth')
        camera_transform = carla.Transform(carla.Location(x=7, z=5))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to = vehicle)
        actor_list.append(camera)
        print('created %s' % camera.type_id)
        cc = carla.ColorConverter.LogarithmicDepth
        #Save depth image to disk
        camera.listen(lambda image: image.save_to_disk('_out2/%06d.png' % image.frame_number, cc))

        # Move vehicle on the map
        location = vehicle.get_location()
        location.y -= 10
        vehicle.set_location(location)
        print('moved vehicle to %s' % location)
        time.sleep(1)

    finally:
        final = {
            "timestamp": objects
            }
        with open("data_file.json", "w") as write_file:
            json.dump(final, write_file)
        print('destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    main(callback)
