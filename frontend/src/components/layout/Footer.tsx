export default function Footer() {
  return (
    <footer className="bg-card border-t border-border px-6 py-4 mt-auto">
      <div className="container mx-auto text-center text-sm text-muted-foreground">
        <p>
          Deep Search Pipeline &copy; {new Date().getFullYear()} · 
          <span className="text-primary"> NSL Ecosystem</span>
        </p>
      </div>
    </footer>
  )
}
