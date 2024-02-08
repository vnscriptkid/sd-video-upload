'use client';

import { useSearchParams } from "next/navigation";

const BUCKET_NAME = 'video-processed-bucket';

export default function Watch() {
  const videoPrefix = `https://storage.googleapis.com/${BUCKET_NAME}/`;
  const videoSrc = useSearchParams().get('v');

  return (
    <div>
      <h1>Watch Page</h1>
      { <video controls src={videoPrefix + videoSrc}/> }
    </div>
  );
  }