import { useState } from 'react'

interface KebabMenuItem {
  label: string
  onClick: () => void
  variant?: 'default' | 'danger' | 'success'
}

const variantClass: Record<NonNullable<KebabMenuItem['variant']>, string> = {
  default: 'text-gray-700 hover:bg-gray-50',
  danger: 'text-red-600 hover:bg-red-50',
  success: 'text-green-600 hover:bg-green-50',
}

export default function KebabMenu({ items }: { items: KebabMenuItem[] }) {
  const [isOpen, setIsOpen] = useState(false)

  if (items.length === 0) return null

  return (
    <div className="relative inline-flex">
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="text-gray-400 hover:text-gray-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors text-lg"
        aria-label="actions"
      >
        ⋮
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 bottom-full mb-1 z-20 bg-white border border-gray-200 rounded-lg shadow-lg py-1 min-w-[140px]">
            {items.map((item) => (
              <button
                key={item.label}
                onClick={() => { item.onClick(); setIsOpen(false) }}
                className={`w-full text-left px-4 py-2 text-sm transition-colors ${variantClass[item.variant ?? 'default']}`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
