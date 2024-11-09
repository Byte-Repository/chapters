#!/bin/bash

# Step 1: Unload v4l2loopback if it's already loaded
echo "Unloading v4l2loopback..."
sudo rmmod v4l2loopback 2>/dev/null

# Step 2: List video devices before enabling loopback
echo "Existing video devices:"
ls /dev/video*

# Step 3: Activate v4l2loopback
echo "Activating v4l2loopback..."
sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2

# Step 4: List video devices after enabling loopback
echo "New video devices:"
ls /dev/video*

# Step 5: Unmount the camera if it's automatically mounted
CAMERA_MOUNT=$(lsblk -o MOUNTPOINT,NAME | grep -i 'camera' | awk '{print $2}')
if [ -n "$CAMERA_MOUNT" ]; then
    echo "Unmounting camera at /dev/$CAMERA_MOUNT..."
    udisksctl unmount -b /dev/$CAMERA_MOUNT
else
    echo "No camera detected as mounted."
fi

# Step 6: Detect the camera
echo "Detecting camera..."
gphoto2 --auto-detect

# Step 7: Stream video from the DSLR to the virtual webcam
echo "Starting video capture..."
gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video0

# Inform the user
echo "DSLR camera is now streaming to /dev/video0. You can now use it in Zoom or OBS."

