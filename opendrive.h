#pragma once
//I haave used the carla opendrive parser. You must change the path of the Opendrive header file according to your system
#include "parser/OpenDriveParser.h"

#include <istream>
#include <ostream>
#include <string>

static void getParser(const std::string &file, XmlInputType inputType, std::string *out_error);
