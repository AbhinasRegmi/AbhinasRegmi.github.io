local M = {}

local function GetFileName()
  local file_name = vim.api.nvim_buf_get_name(0)
  local ext = file_name:match '^.+%.(.+)$'
  return ext
end

local function GetAllVariables()
  local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)
  local variables = {}

  for _, line in ipairs(lines) do
    local key, value = line:match '^@([%w_]+)%s*=%s*(.+)$'
    if key and value then
      variables[key] = value
    else
      -- Stop parsing when the first non-variable line is encountered
      break
    end
  end

  return variables
end

local function Trim(s)
  return (s:gsub('^%s*(.-)%s*$', '%1'))
end

local function ReplaceStringVariables(input)
  local variables = GetAllVariables()

  -- Replace patterns like {{username}} with the corresponding value
  return (input:gsub('{{(.-)}}', function(key)
    return variables[key] or error 'Variable ' .. key ' not found'
  end))
end

local function GetContentBetweenHashes()
  -- Get the current cursor position
  local cursor_pos = vim.api.nvim_win_get_cursor(0)
  local current_line = cursor_pos[1] - 1 -- 0-based index

  -- Get all lines in the file
  local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)

  -- Find the start of the first '###'
  local start_line = -1
  for i = current_line, 1, -1 do
    if lines[i]:match '^%s*###' then
      start_line = i
      break
    end
  end

  -- If no start block found, return an empty string
  if start_line == -1 then
    error 'Cannot find delimeter'
  end

  -- Find the end of the next '###'
  local end_line = -1
  for i = current_line, #lines do
    if lines[i]:match '^%s*###' then
      end_line = i
      break
    end
  end

  -- If no end block found, return an empty string
  if end_line == -1 then
    error 'Cannot find delimeter'
  end

  -- Collect the content between the '###' blocks
  local content = {}
  for i = start_line + 1, end_line - 1 do
    if not (Trim(lines[i]) == '') then
      table.insert(content, ReplaceStringVariables(lines[i]))
    end
  end

  return table.concat(content, '\n')
end

function SplitWindowAndFocus(hashcontent)
  -- split window vertically
  vim.cmd 'vsplit'
  -- open a new empty buffer
  vim.cmd 'enew'

  -- get the buffer name
  local newBuff = vim.api.nvim_get_current_buf()

  -- set name for the buffer
  vim.api.nvim_buf_set_name(newBuff, 'curl_buffer')

  -- write to the buffer
  vim.api.nvim_buf_set_lines(newBuff, 0, -1, false, vim.split(hashcontent, '\n'))

  -- move the cursor to new split
  vim.cmd 'wincmd l'

  -- make the buffer readonly
  vim.bo.readonly = true
  vim.bo.modifiable = false
end

local function RunCurlForSelected()
  if GetFileName() == 'curl' then
    local command = GetContentBetweenHashes()
    local commandOutput = vim.fn.system(command)
    local formattedOutput = vim.fn.system(string.format("echo '%s' | jq .", commandOutput))

    SplitWindowAndFocus(formattedOutput .. '\n\n\n\n' .. '---' .. '\n' .. commandOutput)
  end
end

function M.main()
  RunCurlForSelected()
end

return M
