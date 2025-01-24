"use server";

import Dashboard from "@/components/custom/Dashboard";
import { createUser } from "./actions/createUser";
import { userExists } from "./actions/userExists";
import uploadVideoMetaData from "./actions/uploadVideoMetaData";

export default async function Home() {
  return (
    <Dashboard createUser={createUser} userExists={userExists} uploadVideoMetaData={uploadVideoMetaData}/>
  );
}
