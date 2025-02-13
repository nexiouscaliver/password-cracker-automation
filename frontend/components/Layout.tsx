import Link from "next/link"
import { Button } from "@/components/ui/button"
import type React from "react" // Added import for React
import type { JSX } from "react"

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-gray-800 text-white p-4">
        <nav className="container mx-auto flex justify-between items-center">
          <Link href="/" className="text-xl font-bold">
            Password Analyzer
          </Link>
          <div className="space-x-4">
            <Button asChild>
              <Link href="/">Home</Link>
            </Button>
            <Button asChild>
              <Link href="/submit-hash">Analyze</Link>
            </Button>
            <Button asChild>
              <Link href="/settings">Settings</Link>
            </Button>
          </div>
        </nav>
      </header>

      <main className="flex-grow">{children}</main>

      <footer className="bg-gray-800 text-white p-4 mt-8">
        <div className="container mx-auto text-center">
          <p>&copy; 2024 Password Strength Analyzer. All rights reserved.</p>
          <div className="mt-2">
            <Link href="#" className="hover:underline">
              Documentation
            </Link>
            {" | "}
            <Link href="#" className="hover:underline">
              GitHub
            </Link>
            {" | "}
            <Link href="#" className="hover:underline">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  )
}

