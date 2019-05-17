# Udacity Self-Driving Car Engineer Nanodegree

- [Introduction](#motivation)
- [System Architecture](#arch)
- [Project Structure](#str)
- [Implementation](#imp)
- [Setup and Installation](#Setup)

<a name="motivation"></a>
### Capstone Project - System Integration
<p align="justify">
This project is the final project of  Udacity Self-Driving Car Engineer Nanodegree. Each modules in a self driving car such as perception, path planning and control is implemented as induvidual nodes in the ROS implementation. Induvidual functionalities communicating with other nodes contributes to the full functioning of the self driving car. 
</p>

<a name="arch"></a>
### System Architecture
The following system architecture diagram shows the ROS nodes and topics used in the project.

![image](https://user-images.githubusercontent.com/37708330/57636758-1775d880-75aa-11e9-88ce-f16026764a9f.png)

<a name="str"></a>
### Project Structure

The project is divided into three modules : 1. Perception 2. Planning 3. Control. As the name suggests, the perception module is responsible for the
perception based data processing. By using the perception data, traffic lights and obstacles are detected. In this project, the camera is the only perception
sensor used to accomplish the goal. 

#### waypoint_updater

This package contains the waypoint updater node: waypoint_updater.py. The purpose of this node is to update the target velocity property of each waypoint based on traffic light and obstacle detection data. This node will subscribe to the /base_waypoints, /current_pose, /obstacle_waypoint, and /traffic_waypoint topics, and publish a list of waypoints ahead of the car with target velocities to the /final_waypoints topic.

![image](https://user-images.githubusercontent.com/37708330/57873837-83a54600-780f-11e9-9b9c-7ef44e22a12c.png)

#### twist_controller
Carla is equipped with a drive-by-wire (dbw) system, meaning the throttle, brake, and steering have electronic control. This package contains the files that are responsible for control of the vehicle: the node dbw_node.py and the file twist_controller.py, along with a pid and lowpass filter that you can use in your implementation. The dbw_node subscribes to the /current_velocity topic along with the /twist_cmd topic to receive target linear and angular velocities. Additionally, this node will subscribe to /vehicle/dbw_enabled, which indicates if the car is under dbw or driver control. This node will publish throttle, brake, and steering commands to the /vehicle/throttle_cmd, /vehicle/brake_cmd, and /vehicle/steering_cmd topics.

![image](https://user-images.githubusercontent.com/37708330/57873846-8869fa00-780f-11e9-8a30-5d23d902b0b4.png)

#### tl_detector
This package contains the traffic light detection node: tl_detector.py. This node takes in data from the /image_color, /current_pose, and /base_waypoints topics and publishes the locations to stop for red traffic lights to the /traffic_waypoint topic.The /current_pose topic provides the vehicle's current position, and /base_waypoints provides a complete list of waypoints the car will be following.

We implement both a traffic light detection node and a traffic light classification node. Traffic light detection should take place within tl_detector.py, whereas traffic light classification should take place within ../tl_detector/light_classification_model/tl_classfier.py.

![image](https://user-images.githubusercontent.com/37708330/57873819-7d16ce80-780f-11e9-81cb-936421bd18df.png)

<a name="imp"></a>
### Implementation

There are two tasks that are performed by traffic light detection node:
<p align="justify">
1. Use the vehicle's location and the ```(x, y)``` coordinates for traffic lights to find the nearest visible traffic light ahead of the vehicle. This takes place in the ```process_traffic_lights``` method of ```tl_detector.py```. To find the closest waypoints to the vehicle and lights, ```get_closest_waypoint``` method is used.
Using these waypoint indices, we determine which light is ahead of the vehicle along the list of waypoints. </p>

2. Use the camera image data to classify the color of the traffic light. The core functionality of this step takes place in the ```get_light_state``` method of ```tl_detector.py```.
In order to train the classifier [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) is used.

#### Object Detection by Tensorflow
Tensorflow comes with a default set of demo and utility files. Here this [object_detection_tutorial](https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb) is followed to load and predict the classification. The utility file [label_map_util](https://github.com/tensorflow/models/blob/master/research/object_detection/utils/label_map_util.py) is for loading the label map and converting it as a look up dictioinary. The model is saved as a frozen graph and then it gets loaded. This [article](https://medium.com/@prasadpal107/saving-freezing-optimizing-for-inference-restoring-of-tensorflow-models-b4146deb21b5
) explains completely how frozen graph files can be loaded and saved for further tunning.

#### Object Classification 
run_inference_for_single_image(self, image) functions gets induvidual images and outputs the classified object dictionary variable from the graph. It is possible to run inference on batch of images depending on computational power of GPU and size of the images. Finally get_classification functions returns the state of the traffic light detected.


<a name="Setup"></a>
## Original Setup and Installation Instructions

This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images
