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
    } else {
      console.error("Webcam not initialized");
    }
  }, [webcamRef]);

  const handleTakePhoto = async () => {
    capturePhoto();
    if (img) {
      console.log("Picture Source:", img);
      sendPhoto(img);
    }
  };

  const sendPhoto = async (photoBase64: string) => {
    try {
      if (!photoBase64) {
        console.error("Photo not captured");
        return;
      }

      const response = await axios.post(
        "http://localhost:3000/api/analyze-photo",
        {
          image: photoBase64,
        }
      );

      if (response.status === 200) {
        const data = response.data;
        setApiResponse(data);
      } else {
        console.error("Failed to analyze photo");
      }
    } catch (error) {
      console.error("Error uploading photo:", error);
    }
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

        {apiResponse && (
          <div className="bg-gray-100 p-4 rounded mt-4">
            <Typography variant="h6" gutterBottom>
              API Response:
            </Typography>
            <Typography variant="body1">{apiResponse}</Typography>
          </div>
        )}
      </div>
    </Container>
  );
}
