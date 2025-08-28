# ArUco Marker Models for Gazebo

This repository helps you **generate ArUco markers** and convert them into **Gazebo-compatible models**.  

---

## 📌 Step 1: Generate ArUco Marker Images

Run the following script:

```bash
python3 aruco_marker_create.py
```

This will create ArUco markers as `.png` files.  
The generated images will be saved in:

```bash
gazebo_models-master/ar_tags/images
```

⚠️ **Important:**

- Delete any existing markers in the folder before generating new ones.  
- The markers are generated using OpenCV’s ArUco dictionary.  
- You can select different dictionaries depending on your requirement:  

| Dictionary      | Markers Available | Grid Size |
|-----------------|------------------|-----------|
| DICT_4X4_50     | 50               | 4×4 bits |
| DICT_5X5_100    | 100              | 5×5 bits |
| DICT_6X6_250    | 250              | 6×6 bits |
| DICT_7X7_1000   | 1000             | 7×7 bits |

## 📌 Step 2: Convert Images to Gazebo Models

Run the following command:

```bash
python3 generate_markers_model.py -i <path_to_image_folder> -g <path_to_output_folder> -s <model_size> -w <contour_width>
```
for example
```bash
python3 generate_markers_model.py \
-i /home/.../gazebo_models-master/ar_tags/images \
-g /home/.../Projects/gazebo_models \
-s 700 \
-w 50
```
Arguments:

-i → Path to the image folder containing ArUco markers

-g → Path to the output folder (Gazebo models will be saved here)

-s → Size of the model (e.g., 700)

-w → Contour width of the model (e.g., 50)

## 📌 Step 3: Use Models in Gazebo

Set the output folder as your local Gazebo models folder, so Gazebo can detect them.

Once generated, you can add the models into your Gazebo world.
