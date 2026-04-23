#include <math.h> // need for truncating
#include "Arduino_BMI270_BMM150.h" // the main library

struct pseudoArray
{
  float x;
  float y;
  float z;
  bool newData;
};

pseudoArray IMUreader() 
{
  pseudoArray position;
  position.newData = false;
  if (IMU.accelerationAvailable()) 
  {
    IMU.readAcceleration(position.x, position.y, position.z); // getting the data
    position.newData = true;
  }

  position.x = trunc((position.x*100) + 5000000); // editing the value to correct parameters
  position.y = trunc((position.y*100) + 5000000);
  position.z = trunc((position.z*100) + 5000000);
  if (position.x < 0)
  {
    position.x = 0;
  }
    if (position.y < 0)
  {
    position.y = 0;
  }
    if (position.z < 0)
  {
    position.z = 0;
  }

  return position;

}
