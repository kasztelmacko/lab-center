export type Body_login_login_access_token = {
  grant_type?: string | null
  username: string
  password: string
  scope?: string
  client_id?: string | null
  client_secret?: string | null
}

export type HTTPValidationError = {
  detail?: Array<ValidationError>
}

export type ItemCreate = {
  item_name: string
  quantity?: number
  item_img_url?: string | null
  item_vendor?: string | null
  item_params?: string | null
  lab_id: string
}

export type ItemPublic = {
  item_name: string
  quantity?: number
  item_img_url?: string | null
  item_vendor?: string | null
  item_params?: string | null
  lab_id: string
  item_id: string
}

export type ItemUpdate = {
  item_name?: string | null
  quantity?: number | null
  item_img_url?: string | null
  item_vendor?: string | null
  item_params?: string | null
  lab_id?: string | null
}

export type ItemsPublic = {
  data: Array<ItemPublic>
  count: number
}

export type Message = {
  message: string
}

export type NewPassword = {
  token: string
  new_password: string
}

export type Token = {
  access_token: string
  token_type?: string
}

export type UpdatePassword = {
  current_password: string
  new_password: string
}

export type UserCreate = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password: string
}

export type UserPublic = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  user_id: string
}

export type UserRegister = {
  email: string
  password: string
  full_name?: string | null
}

export type UserUpdate = {
  email?: string | null
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password?: string | null
}

export type UserUpdateMe = {
  full_name?: string | null
  email?: string | null
}

export type UsersPublic = {
  data: Array<UserPublic>
  count: number
}

export type ValidationError = {
  loc: Array<string | number>
  msg: string
  type: string
}

export type LabCreate = {
  lab_place?: string | null
  lab_university?: string | null
  lab_num?: string | null
}

export type LabPublic = {
  lab_place?: string | null
  lab_university?: string | null
  lab_num?: string | null
  lab_id: string
  owner_id: string
}

export type LabUpdate = {
  lab_place?: string | null
  lab_university?: string | null
  lab_num?: string | null
  lab_id: string
  owner_id: string
}

export type LabsPublic = {
  data: Array<LabPublic>
  count: number
}

export type UserLab = {
  userlab_id: string
  user_id: string
  lab_id: string
  can_edit_lab: boolean
  can_edit_items: boolean
  can_edit_users: boolean
}

export type AddUsersToLab = {
  email: string
  can_edit_lab?: boolean
  can_edit_items?: boolean
  can_edit_users?: boolean
  lab_id: string
}

export type UpdateUserLab = {
  can_edit_lab?: boolean
  can_edit_items?: boolean
  can_edit_users?: boolean
}

export type UserLabPublic = {
  userlab_id: string
  user_id: string
  lab_id: string
  can_edit_lab: boolean
  can_edit_items: boolean
  can_edit_users: boolean
}

export type UserLabsPublic = {
  data: Array<UserLabPublic>
  count: number
}

export type RemoveUsersFromLab = {
  user_ids: Array<string>
}

export type BorrowCreate = {
  start_date: string
  end_date?: string | null
  table_name?: string | null
  system_name?: string | null
}

export type TokenPayload = {
  sub?: string | null
}