#include "opendrive.h"
#include "plycpp.h"
#include <iostream>
#include <fstream>

static void getParser(const std::string &file, XmlInputType inputType, std::string *out_error,plycpp::PLYData data,int size){

  carla::opendrive::types::OpenDriveData open_drive_road;
  OpenDriveParser::Parse(file.c_str(), open_drive_road, inputType, out_error);

  // Cartesian coordinates of the point cloud
  auto vertexElement = data["vertex"];
  const float* ptX = vertexElement->properties["x"]->ptr<float>();
	const float* ptY = vertexElement->properties["y"]->ptr<float>();
  const float* ptZ = vertexElement->properties["z"]->ptr<float>();

  std::cout << std::endl << "Traffic Signs" << std::endl;
  for(int i=0;i<open_drive_road.roads.size();i++){

    double x_road,y_road,x_signal,y_signal;
    // X,Y coordinates of the roads
    x_road=open_drive_road.roads[i].geometry_attributes[0]->start_position_x;
    y_road=open_drive_road.roads[i].geometry_attributes[0]->start_position_y;

    for(int j=0;j<open_drive_road.roads[i].trafic_signals.size();j++){

      //X,Y coordinates of the traffic signals on the ith road
      x_signal = x_road - open_drive_road.roads[i].trafic_signals[j].track_position+9.5;
      y_signal = y_road + open_drive_road.roads[i].trafic_signals[j].start_position;
      std::cout << open_drive_road.roads[i].trafic_signals[j].name <<" "<< x_signal<<" "<<y_signal <<" "<< std::endl;

      for(size_t k=0;k<size;k++){
        if((abs(x_signal-(ptX[k]+13.375)<=0.05)) && (abs(-y_signal-(ptY[k]-20)<=0.05))){
          std::cout<<ptX[k]+13.375 <<" "<<-(ptY[k]-20)<<" "<<ptZ[k]+0.5<<std::endl;

        }
      }
      std::cout<<std::endl;
    }
    std::cout << std::endl << "Road Markings" << std::endl;
    for(int i=0;i<20;i++){

      double y_start = 2.5+10*i;
      double y_end = y_start+5;
      double x_start = 5.75-0.06+9.5;
      double x_end = 5.75+0.06+9.5;
      // Road markings on the ith road
      if((ptX[k]+13.375>x_start && ptX[k]+13.375<x_end) && (-ptY[k]+20>y_start && -ptY[k]+20<y_start )){
        std::cout<<ptX[k]+13.375 <<" "<<-(ptY[k]-20)<<" "<<ptZ[k]+0.5<<std::endl;
      }
    }
  }

}

int main(){
  std::string file = "mercedes/road_specification_v3.xodr";
  std::string out_error;

  plycpp::PLYData data;     // takes point cloud into buffer
  plycpp::load("out/173262.ply", data);
  int size=0;
  for (const auto& element : data)
			{
				size = element.data->size();
			}
  getParser(file,XmlInputType::FILE,&out_error,data,size);    // Parses the xodr file and gets the final segmented output
}
