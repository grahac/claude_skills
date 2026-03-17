# Elixir-Specific Simplification Patterns

## Pattern Matching
```elixir
# Before
def get_name(user) do
  if user != nil do
    user.name
  else
    nil
  end
end

# After
def get_name(nil), do: nil
def get_name(%{name: name}), do: name
```

## Pipeline Clarity
```elixir
# Before - overly nested
result = Enum.map(Enum.filter(list, fn x -> x > 0 end), fn x -> x * 2 end)

# After - pipeline
result =
  list
  |> Enum.filter(&(&1 > 0))
  |> Enum.map(&(&1 * 2))
```

## With Statements
```elixir
# Before - nested case statements
case do_thing() do
  {:ok, result} ->
    case do_other(result) do
      {:ok, final} -> {:ok, final}
      {:error, reason} -> {:error, reason}
    end
  {:error, reason} -> {:error, reason}
end

# After - with statement
with {:ok, result} <- do_thing(),
     {:ok, final} <- do_other(result) do
  {:ok, final}
end
```

## Guard Clauses
```elixir
# Before
def process(value) do
  if is_integer(value) and value > 0 do
    value * 2
  else
    {:error, :invalid}
  end
end

# After
def process(value) when is_integer(value) and value > 0 do
  value * 2
end
def process(_), do: {:error, :invalid}
```
