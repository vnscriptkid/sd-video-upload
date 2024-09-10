'use client';

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

const BUCKET_NAME = 'video-processed-bucket';

function _Watch() {
  const videoPrefix = `https://storage.googleapis.com/${BUCKET_NAME}/`;
  const videoSrc = useSearchParams().get('v');

  return (
    <div>
        <h1>Watch Page</h1>
        { <video controls src={videoPrefix + videoSrc}/> }
      </div>
  )
}

export default function Watch() {

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <_Watch />
    </Suspense>
  );
  }