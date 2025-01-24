"use server";

import Dashboard from "@/components/custom/Dashboard";
import { createUser } from "./actions/createUser";
import { userExists } from "./actions/userExists";

export default async function Home() {
  return (
    <Dashboard createUser={createUser} userExists={userExists} />
  );
}
