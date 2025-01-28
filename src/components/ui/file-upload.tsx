"use client"
import type React from "react"
import { useRef } from "react"
import { motion } from "framer-motion"
import { IconUpload } from "@tabler/icons-react"
import { arrayBuffer } from "stream/consumers"

const buttonVariant = {
  initial: { y: 0 },
  hover: { y: -5 },
}

export const FileUpload = ({
  onChange,
}: {
  onChange?: (file: File) => void
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    onChange && onChange(file)
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="relative">
      <motion.button
        onClick={handleClick}
        variants={buttonVariant}
        initial="initial"
        whileHover="hover"
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
        className="bg-white dark:bg-neutral-800 rounded-full p-4 shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        aria-label="Upload file"
      >
        <IconUpload className="h-6 w-6 text-blue-500 dark:text-blue-400" />
      </motion.button>
      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
        className="hidden"
        accept="video/*"
        aria-hidden="true"
      />
    </div>
  )
}

