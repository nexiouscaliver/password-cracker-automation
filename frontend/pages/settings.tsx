"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Switch } from "@/components/ui/switch"
import { Button } from "@/components/ui/button"
import { updateSettings } from "@/utils/api"
import { toast } from "@/components/ui/use-toast"
import type React from "react" // Added import for React

export default function Settings() {
  const [settings, setSettings] = useState({
    bruteForce: true,
    dictionaryAttack: true,
    rainbowTable: true,
    hybridAttack: true,
    maskAttack: true,
  })
  const [file, setFile] = useState<File | null>(null)

  const handleToggle = (technique: string) => {
    setSettings((prev) => ({ ...prev, [technique]: !prev[technique as keyof typeof prev] }))
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0]
    if (uploadedFile) {
      if (uploadedFile.type !== "text/plain") {
        toast({
          title: "Invalid file type",
          description: "Please upload a .txt file",
          variant: "destructive",
        })
        return
      }
      if (uploadedFile.size > 5 * 1024 * 1024) {
        // 5MB limit
        toast({
          title: "File too large",
          description: "Please upload a file smaller than 5MB",
          variant: "destructive",
        })
        return
      }
      setFile(uploadedFile)
    }
  }

  const handleSave = async () => {
    try {
      await updateSettings({ ...settings, customDictionary: file })
      toast({
        title: "Settings saved",
        description: "Your settings have been updated successfully",
      })
    } catch (error) {
      console.error("Failed to save settings:", error)
      toast({
        title: "Error",
        description: "Failed to save settings. Please try again.",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Settings</CardTitle>
          <CardDescription>Customize your password cracking techniques and options</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <h3 className="text-lg font-medium mb-2">Cracking Techniques</h3>
            {Object.entries(settings).map(([technique, enabled]) => (
              <div key={technique} className="flex items-center justify-between py-2">
                <Label htmlFor={technique}>{technique}</Label>
                <Switch id={technique} checked={enabled} onCheckedChange={() => handleToggle(technique)} />
              </div>
            ))}
          </div>

          <div>
            <h3 className="text-lg font-medium mb-2">Custom Dictionary</h3>
            <Input type="file" onChange={handleFileUpload} accept=".txt" />
            <p className="text-sm text-gray-500 mt-1">Upload a custom dictionary file (txt format, max 5MB)</p>
          </div>

          <Button onClick={handleSave}>Save Settings</Button>
        </CardContent>
      </Card>
    </div>
  )
}

