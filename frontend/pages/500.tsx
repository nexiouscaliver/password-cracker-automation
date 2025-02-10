import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function Custom500() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-6xl font-bold mb-4">500</h1>
      <p className="text-xl mb-8">Oops! Something went wrong on our end</p>
      <Button asChild>
        <Link href="/">Go back home</Link>
      </Button>
    </div>
  )
}

