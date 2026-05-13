# UI Patterns

Common UI patterns used across the frontend. These are reusable building blocks that appear in multiple pages.

---

## Kebab Menu (3-dot Action Menu)

Used on list pages where each row has multiple actions. Instead of showing all action buttons inline, a single `⋮` button opens a small dropdown menu.

### When to use

- A row has 2+ actions
- Actions have different urgency (e.g. destructive vs. neutral)
- Showing all buttons inline clutters the row

### Structure

```tsx
<div className="relative flex justify-end">
  {/* Trigger button */}
  <button
    onClick={() => setOpenMenuId(openMenuId === item.id ? null : item.id)}
    className="text-gray-400 hover:text-gray-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors text-lg"
    aria-label="actions"
  >
    ⋮
  </button>

  {openMenuId === item.id && (
    <>
      {/* Invisible overlay — closes menu on outside click */}
      <div
        className="fixed inset-0 z-10"
        onClick={() => setOpenMenuId(null)}
      />

      {/* Menu */}
      <div className="absolute right-0 bottom-full mb-1 z-20 bg-white border border-gray-200 rounded-lg shadow-lg py-1 min-w-[140px]">
        <button
          onClick={() => { handleEdit(item.id); setOpenMenuId(null) }}
          className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Edit name
        </button>
        <button
          onClick={() => { handleDeactivate(item.id); setOpenMenuId(null) }}
          className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
        >
          Deactivate
        </button>
      </div>
    </>
  )}
</div>
```

### How it works

- `openMenuId` tracks which row's menu is open — only one can be open at a time
- Clicking `⋮` toggles: if the same row is clicked again, it closes
- The `fixed inset-0` overlay sits behind the menu and in front of everything else — clicking anywhere outside hits the overlay and closes the menu
- Menu items call their handler then immediately close the menu with `setOpenMenuId(null)`
- `aria-label="actions"` makes the button accessible and testable

### State location

`openMenuId` lives in the hook (not in the component) to follow the established pattern where hooks own all state:

```ts
const [openMenuId, setOpenMenuId] = useState<string | null>(null)
```

### Tests

To test actions inside the menu, first open the menu then click the action:

```tsx
await userEvent.click(screen.getByRole('button', { name: /actions/i }))
await userEvent.click(screen.getByRole('button', { name: /deactivate/i }))
```

---

## Table with Dropdown Menu

Tables with `overflow-hidden` on the container clip absolutely positioned elements (like dropdown menus). When a table row has a dropdown, remove `overflow-hidden` and instead apply rounded corners to the `th` cells:

```tsx
{/* ❌ Clips dropdowns */}
<div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th className="text-right">Actions</th>
      </tr>
    </thead>

{/* ✅ Allows dropdowns, rounds header corners */}
<div className="bg-white rounded-xl border border-gray-200 shadow-sm">
  <table>
    <thead>
      <tr>
        <th className="rounded-tl-xl">Name</th>
        <th className="text-right rounded-tr-xl">Actions</th>
      </tr>
    </thead>
```

The border and shadow still show a rounded box. The first `th` gets `rounded-tl-xl`, the last gets `rounded-tr-xl`. This achieves the same visual result without clipping absolutely positioned children.

---

## Inline Edit in a Table Row

Used when a single field needs to be editable without opening a separate page or modal. The cell switches between display and edit mode based on an `editingId` state.

```tsx
<td>
  {editingId === item.id ? (
    <input
      value={editingName}
      onChange={(e) => setEditingName(e.target.value)}
      className="border border-gray-300 rounded px-2 py-1 text-sm w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  ) : (
    <span className="font-medium text-gray-900">{item.name}</span>
  )}
</td>
<td className="text-right">
  {editingId === item.id ? (
    <div className="flex justify-end gap-2">
      <button onClick={handleUpdate}>Save</button>
      <button onClick={cancelEdit}>Cancel</button>
    </div>
  ) : (
    {/* ⋮ menu with Edit option */}
  )}
</td>
```

`editingId` is `string | null` — `null` means nothing is being edited, a string means that row is in edit mode. Only one row can be in edit mode at a time.

---

## Status Badge

Used to show active/inactive state consistently across all list pages:

```tsx
<span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium border ${
  item.is_active
    ? 'bg-green-50 text-green-700 border-green-100'
    : 'bg-gray-100 text-gray-500 border-gray-200'
}`}>
  {item.is_active ? 'Active' : 'Inactive'}
</span>
```
