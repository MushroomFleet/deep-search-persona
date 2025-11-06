export default function Footer() {
  return (
    <footer className="bg-card border-t border-border px-6 py-4 mt-auto">
      <div className="container mx-auto text-center text-sm text-muted-foreground">
        <p>
          &copy; {new Date().getFullYear()},{' '}
          <a 
            href="https://www.scuffedepoch.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-primary hover:underline"
          >
            SCUFFEDEPOCH
          </a>
          {' '}&trade;
        </p>
      </div>
    </footer>
  )
}
