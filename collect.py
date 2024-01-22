import cv2
import os

class RTSPImageCapture:
    def __init__(self, rtsp_url, output_dir):
        self.rtsp_url = rtsp_url
        self.output_dir = output_dir
        self.cap = None
        self.image_count = 0

    def open_stream(self):
        # Create a VideoCapture object to connect to the RTSP stream
        self.cap = cv2.VideoCapture(self.rtsp_url)

        # Check if the VideoCapture object was successfully created
        if not self.cap.isOpened():
            print("Error: Could not open RTSP stream.")
            exit()

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def capture_images(self):
        while True:
            # Capture a frame from the RTSP stream
            ret, frame = self.cap.read()

            # Check if the frame was captured successfully
            if not ret:
                print("Error: Could not read frame from RTSP stream.")
                break

            # Save the frame as a JPG image
            image_filename = os.path.join(self.output_dir, f'image_{self.image_count:04d}.jpg')
            cv2.imwrite(image_filename, frame)

            # Increment the image count
            self.image_count += 1

            # Display the captured frame (optional)
            cv2.imshow('Captured Frame', frame)

            # Exit the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_stream(self):
        # Release the VideoCapture object and close the OpenCV window
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()

    def main(self):
        try:
            self.open_stream()
            self.capture_images()
        finally:
            self.close_stream()

if __name__ == "__main__":
    # Define the RTSP stream URL and output directory
    rtsp_url = 'rtsp://your_rtsp_stream_url'
    output_dir = 'rivereye005_cam1_data'

    # Create an instance of the RTSPImageCapture class
    image_capture = RTSPImageCapture(rtsp_url, output_dir)

    # Run the main function of the class
    image_capture.main()
