This is the solution to Question 2.

The custom_ik_teleop.py file i used is attached below .

Also changes are made in setup.py :
```python
entry_points={
    'console_scripts': [
        'custom_ik_teleop = bme_ros2_simple_arm_py.custom_ik_teleop:main',
    ],
},
The drive link to video is :
https://drive.google.com/file/d/1GCoTs6oQJhCLaBA2xpwGcd2FP49Thq4E/view?usp=drive_link
