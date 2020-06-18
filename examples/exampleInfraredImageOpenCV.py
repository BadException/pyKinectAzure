import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.0\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

if __name__ == "__main__":

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Modify camera configuration
	device_config = pyKinectAzure.config()
	device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
	device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
	print(device_config)

	# Start cameras using modified configuration
	pyK4A.device_start_cameras(device_config)

	cv2.namedWindow('Infrared Image',cv2.WINDOW_NORMAL)

	k = 0
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the color image from the capture
		ir_image_handle = pyK4A.capture_get_ir_image()

		# Check the image has been read correctly
		if ir_image_handle:

			# Read and convert the image data to numpy array:
			ir_image = pyK4A.image_convert_to_numpy(ir_image_handle)

			# Convert to 0-255 range and saturate over 4000 pixel value
			image_to_show = ir_image*1
			image_to_show[image_to_show>4000] = 4000
			image_to_show = np.round(image_to_show/16).astype(np.uint8)

			# Plot the image
			cv2.imshow('Infrared Image',image_to_show)
			k = cv2.waitKey(25)

			# Release the image
			pyK4A.image_release(ir_image_handle)

		pyK4A.capture_release()

		if k==27:    # Esc key to stop
			break

	pyK4A.device_stop_cameras()
	pyK4A.device_close()