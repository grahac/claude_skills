# Removing Duplicate Code — Examples

## Extract Shared Functions
```elixir
# Before - duplicated in multiple modules
defmodule UserLive.Index do
  def format_date(date) do
    Calendar.strftime(date, "%B %d, %Y")
  end
end

defmodule OrderLive.Index do
  def format_date(date) do
    Calendar.strftime(date, "%B %d, %Y")
  end
end

# After - extract to shared helper
defmodule MyAppWeb.Helpers do
  def format_date(date) do
    Calendar.strftime(date, "%B %d, %Y")
  end
end

# Then import where needed
import MyAppWeb.Helpers, only: [format_date: 1]
```

## Extract Function Components
```elixir
# Before - duplicated template fragments
# In user_live/index.html.heex
<div class="flex items-center gap-2">
  <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
    {String.first(@user.name)}
  </div>
  <span>{@user.name}</span>
</div>

# Same code in team_live/show.html.heex, admin_live/users.html.heex...

# After - extract to component
defmodule MyAppWeb.Components.Avatar do
  use Phoenix.Component

  attr :user, :map, required: true
  attr :size, :string, default: "md"

  def avatar(assigns) do
    ~H"""
    <div class={["flex items-center gap-2", size_class(@size)]}>
      <div class="rounded-full bg-blue-500 flex items-center justify-center text-white">
        {String.first(@user.name)}
      </div>
      <span>{@user.name}</span>
    </div>
    """
  end
end
```

## Extract Common LiveView Patterns
```elixir
# Before - repeated in every LiveView
def handle_info({:flash, type, message}, socket) do
  {:noreply, put_flash(socket, type, message)}
end

def handle_info(:clear_flash, socket) do
  {:noreply, clear_flash(socket)}
end

# After - use a shared behavior or macro
defmodule MyAppWeb.LiveHelpers do
  defmacro __using__(_opts) do
    quote do
      def handle_info({:flash, type, message}, socket) do
        {:noreply, put_flash(socket, type, message)}
      end

      def handle_info(:clear_flash, socket) do
        {:noreply, clear_flash(socket)}
      end

      defoverridable handle_info: 2
    end
  end
end
```

## Consolidate Similar Queries
```elixir
# Before - separate functions doing similar things
def list_active_users do
  User
  |> where([u], u.active == true)
  |> order_by([u], u.name)
  |> Repo.all()
end

def list_inactive_users do
  User
  |> where([u], u.active == false)
  |> order_by([u], u.name)
  |> Repo.all()
end

# After - parameterized function
def list_users(opts \\ []) do
  User
  |> filter_by_status(opts[:status])
  |> order_by([u], u.name)
  |> Repo.all()
end

defp filter_by_status(query, nil), do: query
defp filter_by_status(query, status), do: where(query, [u], u.active == ^(status == :active))
```

## Use Slots for Template Variations
```elixir
# Before - similar templates with slight differences
# card_with_icon.html.heex
<div class="card">
  <.icon name="star" />
  <h3>{@title}</h3>
  <p>{@content}</p>
</div>

# card_with_image.html.heex
<div class="card">
  <img src={@image} />
  <h3>{@title}</h3>
  <p>{@content}</p>
</div>

# After - one component with slots
attr :title, :string, required: true
attr :content, :string, required: true
slot :media

def card(assigns) do
  ~H"""
  <div class="card">
    {render_slot(@media)}
    <h3>{@title}</h3>
    <p>{@content}</p>
  </div>
  """
end
```
