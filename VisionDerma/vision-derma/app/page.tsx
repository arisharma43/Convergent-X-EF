"use client";
import { useRef, useState, useCallback } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import { Button, Container, Typography } from "@mui/material";
import { CloudUpload as CloudUploadIcon } from "@mui/icons-material";

const videoConstraints = {
  width: 400,
  height: 400,
  facingMode: "user",
};

export default function Home() {
  const webcamRef = useRef<Webcam>(null);
  const [img, setImg] = useState<string>("");
  const [apiResponse, setApiResponse] = useState<string>("");

  const capturePhoto = useCallback(() => {
    const currentWebcam = webcamRef.current;
    if (currentWebcam) {
      const pictureSrc = currentWebcam.getScreenshot();
      setImg(pictureSrc || ""); // Ensure an empty string if null

      if (pictureSrc) {
        // Save the image to a folder (you may need to adjust the path)
        const fileName = `photo_${Date.now()}.jpg`;
        const filePath = `/path/to/your/image/folder/${fileName}`;

        // Assuming you have a backend endpoint to handle the file path
        sendFilePathToBackend(filePath);

        // Optionally, you can save the image to the server using a backend API
        saveImageOnServer(pictureSrc, fileName);
      }
    } else {
      console.error("Webcam not initialized");
    }
  }, [webcamRef]);

  const saveImageOnServer = async (photoBase64: string, fileName: string) => {
    try {
      // const response = await axios.post(
      //   "http://127.0.0.1:8000/api/save-image",
      //   {
      //     image: photoBase64,
      //     fileName: fileName,
      //   }
      // );

      if (response.status !== 200) {
        console.error("Failed to save image on server");
      }
    } catch (error) {
      console.error("Error saving image on server:", error);
    }
  };

  const sendFilePathToBackend = async (filePath: string) => {
    try {
      // const response = await axios.post(
      //   "http://127.0.0.1:8000/api/analyze-photo",
      //   {
      //     filePath: filePath,
      //   }
      // );

      if (response.status === 200) {
        // const data = response.data;
        // setApiResponse(JSON.stringify(data));
        // console.log(apiResponse);
      } else {
        console.error("Failed to analyze photo");
      }
    } catch (error) {
      console.error("Error sending file path to backend:", error);
    }
  };

  const handleTakePhoto = () => {
    capturePhoto();
  };

  return (
    <Container component="main" maxWidth="md">
      <div className="flex min-h-screen flex-col items-center justify-between p-24">
        <Typography variant="h5" gutterBottom>
          Photo Analyzer
        </Typography>

        <div className="mb-4">
          {img === "" ? (
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={400}
              videoConstraints={videoConstraints}
            />
          ) : (
            <>
              <img src={img} alt="screenshot" />
              <button onClick={() => setImg("")}>Retake</button>
            </>
          )}
        </div>

        <Button
          variant="contained"
          color="primary"
          startIcon={<CloudUploadIcon />}
          onClick={handleTakePhoto}
        >
          Take Photo
        </Button>

        <div className="bg-gray-100 p-4 rounded mt-4">
          <Typography color="black" variant="h6" gutterBottom>
            API Response:
          </Typography>
          <Typography color="black" variant="body1">
            {"LA MER 4.1 Moisturizer"}
          </Typography>
        </div>
      </div>
    </Container>
  );
}
