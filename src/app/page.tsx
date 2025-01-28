"use server";

import Dashboard from "@/components/custom/Dashboard";
import { createUser } from "./actions/createUser";
import { userExists } from "./actions/userExists";
import uploadVideoMetaData from "./actions/uploadVideoMetaData";
import getVideos from "./actions/getVideos";
import uploadVideo from "./actions/uploadVideo";

export default async function Home() {
  return (
    <Dashboard createUser={createUser} userExists={userExists} uploadVideoMetaData={uploadVideoMetaData} getVideos={getVideos} uploadVideo={uploadVideo}/>
  );
}
