"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useProgress } from "@/context/ProgressContext"
import { getResults } from "@/utils/api"
import { Button } from "@/components/ui/button"
import { Download } from "lucide-react"

interface ResultsData {
  cracked: boolean
  password?: string
  timeTaken: number
  strengthRating: "weak" | "medium" | "strong"
  techniques: Record<string, { success: boolean; timeTaken: number }>
}

export default function Results() {
  const { progress } = useProgress()
  const [results, setResults] = useState<ResultsData | null>(null)

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const data = await getResults()
        setResults(data)
      } catch (error) {
        console.error("Failed to fetch results:", error)
      }
    }

    fetchResults()
  }, [])

  const handleDownload = () => {
    if (!results) return

    const resultsText = `
Password Cracking Results:
Status: ${results.cracked ? "Cracked" : "Not Cracked"}
${results.cracked && results.password ? `Password: ${results.password}` : ""}
Total Time Taken: ${results.timeTaken} seconds
Strength Rating: ${results.strengthRating}

Technique Details:
${Object.entries(results.techniques)
  .map(([technique, data]) => `${technique}: ${data.success ? "Success" : "Failed"} (${data.timeTaken} seconds)`)
  .join("\n")}
    `.trim()

    const blob = new Blob([resultsText], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "password_analysis_results.txt"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (!results) {
    return <div>Loading results...</div>
  }

  return (
    <div className="container mx-auto p-4">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Password Cracking Results</CardTitle>
          <CardDescription>Final analysis of the submitted hash</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <p>
                <strong>Status:</strong>{" "}
                <Badge variant={results.cracked ? "destructive" : "default"}>
                  {results.cracked ? "Cracked" : "Not Cracked"}
                </Badge>
              </p>
              <Button onClick={handleDownload} variant="outline" size="sm">
                <Download className="mr-2 h-4 w-4" /> Download Results
              </Button>
            </div>
            {results.cracked && results.password && (
              <p>
                <strong>Password:</strong> {results.password}
              </p>
            )}
            <p>
              <strong>Total Time Taken:</strong> {results.timeTaken} seconds
            </p>
            <p>
              <strong>Strength Rating:</strong>{" "}
              <Badge
                variant={
                  results.strengthRating === "weak"
                    ? "destructive"
                    : results.strengthRating === "medium"
                      ? "warning"
                      : "success"
                }
              >
                {results.strengthRating}
              </Badge>
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Technique Details</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Technique</TableHead>
                <TableHead>Result</TableHead>
                <TableHead>Time Taken (s)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(results.techniques).map(([technique, data]) => (
                <TableRow key={technique}>
                  <TableCell>{technique}</TableCell>
                  <TableCell>
                    <Badge variant={data.success ? "success" : "secondary"}>
                      {data.success ? "Success" : "Failed"}
                    </Badge>
                  </TableCell>
                  <TableCell>{data.timeTaken}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

