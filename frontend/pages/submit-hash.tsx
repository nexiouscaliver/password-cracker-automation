"use client"

import { useState } from "react"
import { TextRevealCard } from "@/components/ui/text-reveal-card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useRouter } from "next/router"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { submitHash } from "@/utils/api"

export default function SubmitHash() {
  const [hash, setHash] = useState("")
  const [algorithm, setAlgorithm] = useState("")
  const [maxTime, setMaxTime] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!hash || !algorithm) {
      setError("Please fill in all required fields.")
      return
    }

    try {
      await submitHash({ hash, algorithm, maxTime: Number.parseInt(maxTime) || 0 })
      router.push("/dashboard")
    } catch (err) {
      setError("Failed to submit hash. Please try again.")
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <TextRevealCard text="Submit Your Hash" revealText="Let's Analyze It!" className="w-full max-w-md mb-8" />
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <div>
          <Label htmlFor="hash">Hash Value</Label>
          <Input
            id="hash"
            value={hash}
            onChange={(e) => setHash(e.target.value)}
            placeholder="Enter hash value"
            required
          />
        </div>
        <div>
          <Label htmlFor="algorithm">Hashing Algorithm</Label>
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Select value={algorithm} onValueChange={setAlgorithm}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select algorithm" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="md5">MD5</SelectItem>
                    <SelectItem value="sha256">SHA256</SelectItem>
                  </SelectContent>
                </Select>
              </TooltipTrigger>
              <TooltipContent>
                <p>Choose the algorithm used to hash the password</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
        <div>
          <Label htmlFor="maxTime">Maximum Cracking Time (seconds)</Label>
          <Input
            id="maxTime"
            type="number"
            value={maxTime}
            onChange={(e) => setMaxTime(e.target.value)}
            placeholder="Enter max time in seconds"
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <Button type="submit" className="w-full">
          Submit Hash
        </Button>
      </form>
    </div>
  )
}

