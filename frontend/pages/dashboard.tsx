"use client"

import { useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useRouter } from "next/router"
import { useProgress } from "../context/ProgressContext"
import { getProgress } from "../utils/api"
import { Badge } from "@/components/ui/badge"

export default function Dashboard() {
  const { progress, updateProgress } = useProgress()
  const router = useRouter()

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const data = await getProgress()
        updateProgress(data)
      } catch (error) {
        console.error("Failed to fetch progress:", error)
      }
    }

    fetchProgress() // Initial fetch
    const interval = setInterval(fetchProgress, 2000) // Poll every 2 seconds

    return () => clearInterval(interval)
  }, [updateProgress])

  useEffect(() => {
    if (progress.completedTechniques === progress.totalTechniques && progress.totalTechniques > 0) {
      router.push("/results")
    }
  }, [progress, router])

  return (
    <div className="container mx-auto p-4">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Cracking Progress</CardTitle>
          <CardDescription>Real-time updates on password cracking attempts</CardDescription>
        </CardHeader>
        <CardContent>
          <Progress value={(progress.completedTechniques / progress.totalTechniques) * 100} className="mb-4" />
          <p>
            Completed: {progress.completedTechniques} / {progress.totalTechniques}
          </p>
          <p>Remaining: {progress.remainingTechniques}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Technique Results</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Technique</TableHead>
                <TableHead>Result</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(progress.results).map(([technique, result]) => (
                <TableRow key={technique}>
                  <TableCell>{technique}</TableCell>
                  <TableCell>
                    <Badge variant={result === "Success" ? "success" : "destructive"}>{result}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

