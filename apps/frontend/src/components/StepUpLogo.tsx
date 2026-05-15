export function StepUpLogo({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 28 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <rect x="0" y="12" width="7" height="8" rx="1.5" fill="currentColor" opacity="0.55" />
      <rect x="9" y="6" width="7" height="14" rx="1.5" fill="currentColor" opacity="0.8" />
      <rect x="18" y="0" width="7" height="20" rx="1.5" fill="currentColor" />
    </svg>
  )
}
