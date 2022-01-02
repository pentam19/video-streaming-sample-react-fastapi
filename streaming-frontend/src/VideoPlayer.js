import React from "react";
import ReactPlayer from "react-player";

const VideoPlayer = () => {
  return (
    <div>
      <h2>ReactPlayer</h2>
      <ReactPlayer
        //url="http://localhost:8000/video"
        url="http://localhost:8000/stream"
        id="MainPlay"
        playing
        //loop
        controls={true}
        width="960px"
        height="540px"
      />
    </div>
  );
};

export default VideoPlayer;
