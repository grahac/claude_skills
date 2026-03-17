# LiveView-Specific Simplification Patterns

## Assign Pipelines
```elixir
# Before
def mount(_params, _session, socket) do
  socket = assign(socket, :users, [])
  socket = assign(socket, :loading, true)
  socket = assign(socket, :filter, nil)
  {:ok, socket}
end

# After
def mount(_params, _session, socket) do
  {:ok, assign(socket, users: [], loading: true, filter: nil)}
end
```

## Handle Events
```elixir
# Before - pattern match in function body
def handle_event("action", params, socket) do
  case params["type"] do
    "save" -> # save logic
    "delete" -> # delete logic
  end
end

# After - pattern match in function head
def handle_event("save", _params, socket) do
  # save logic
end

def handle_event("delete", %{"id" => id}, socket) do
  # delete logic
end
```

## Stream Over Temporary Assigns
```elixir
# Prefer streams for large lists
def mount(_params, _session, socket) do
  {:ok, stream(socket, :items, Items.list_items())}
end
```
