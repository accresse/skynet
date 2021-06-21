from flask import Flask, render_template, Response
import cv2, imutils

min_area=500

app = Flask(__name__)

#camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
camera = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

def gen_frames1():  # generate frame by frame from camera
	backSub = cv2.createBackgroundSubtractorMOG2()

	while True:
		# Capture frame-by-frame
		success, frame = camera.read()  # read the camera frame
		if not success:
			break
		else:
			fgMask = backSub.apply(frame)
			cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
			cv2.putText(frame, str(camera.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
			ret, buffer = cv2.imencode('.jpg', fgMask)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_frames3():  # generate frame by frame from camera
	dim = None
	firstFrame = None

	while True:
		# Capture frame-by-frame
		success, frame = camera.read()  # read the camera frame
		if not success:
			break
		else:
			if not dim:
				scale_percent = 25 # percent of original size
				width = int(frame.shape[1] * scale_percent / 100)
				height = int(frame.shape[0] * scale_percent / 100)
				dim = (width, height)
				print(dim)
			frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)
			if firstFrame is None:
				firstFrame = gray
			else:
				# compute the absolute difference between the current frame and
				# first frame
				frameDelta = cv2.absdiff(firstFrame, gray)
				thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

				# dilate the thresholded image to fill in holes, then find contours
				# on thresholded image
				thresh = cv2.dilate(thresh, None, iterations=2)
				cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)
				# loop over the contours
				for c in cnts:
					# if the contour is too small, ignore it
					if cv2.contourArea(c) < min_area:
						continue

					# compute the bounding box for the contour, draw it on the frame,
					# and update the text
					(x, y, w, h) = cv2.boundingRect(c)
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

				ret, buffer = cv2.imencode('.jpg', frame)
				frame = buffer.tobytes()
				yield (b'--frame\r\n'
					   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_frames():  # generate frame by frame from camera
	while True:
		# Capture frame-by-frame
		success, frame = camera.read()  # read the camera frame
		if not success:
			break
		else:
			#not sure if grayscale conversion is necessarys
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.1, 4)

			# Draw rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

			ret, buffer = cv2.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
	#Video streaming route. Put this in the src attribute of an img tag
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0')
