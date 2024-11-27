import type { CancelablePromise } from "./core/CancelablePromise"
import { OpenAPI } from "./core/OpenAPI"
import { request as __request } from "./core/request"

import type {
  Body_login_login_access_token,
  Message,
  NewPassword,
  Token,
  UserPublic,
  UpdatePassword,
  UserCreate,
  UserRegister,
  UsersPublic,
  UserUpdate,
  UserUpdateMe,
  ItemCreate,
  ItemPublic,
  ItemsPublic,
  ItemUpdate,
  LabCreate,
  LabPublic,
  LabsPublic,
  LabUpdate,
  AddUsersToLab,
  RemoveUsersFromLab,
  UpdateUserLab,
  BorrowCreate
} from "./models"

export type TDataLoginAccessToken = {
  formData: Body_login_login_access_token
}
export type TDataRecoverPassword = {
  email: string
}
export type TDataResetPassword = {
  requestBody: NewPassword
}
export type TDataRecoverPasswordHtmlContent = {
  email: string
}

export class LoginService {
  /**
   * Login Access Token
   * OAuth2 compatible token login, get an access token for future requests
   * @returns Token Successful Response
   * @throws ApiError
   */
  public static loginAccessToken(
    data: TDataLoginAccessToken,
  ): CancelablePromise<Token> {
    const { formData } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/login/access-token",
      formData: formData,
      mediaType: "application/x-www-form-urlencoded",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Test Token
   * Test access token
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static testToken(): CancelablePromise<UserPublic> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/login/test-token",
    })
  }

  /**
   * Recover Password
   * Password Recovery
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static recoverPassword(
    data: TDataRecoverPassword,
  ): CancelablePromise<Message> {
    const { email } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/password-recovery/{email}",
      path: {
        email,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Reset Password
   * Reset password
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static resetPassword(
    data: TDataResetPassword,
  ): CancelablePromise<Message> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/reset-password/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Recover Password Html Content
   * HTML Content for Password Recovery
   * @returns string Successful Response
   * @throws ApiError
   */
  public static recoverPasswordHtmlContent(
    data: TDataRecoverPasswordHtmlContent,
  ): CancelablePromise<string> {
    const { email } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/password-recovery-html-content/{email}",
      path: {
        email,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export type TDataReadUsers = {
  limit?: number
  skip?: number
}
export type TDataCreateUser = {
  requestBody: UserCreate
}
export type TDataUpdateUserMe = {
  requestBody: UserUpdateMe
}
export type TDataUpdatePasswordMe = {
  requestBody: UpdatePassword
}
export type TDataRegisterUser = {
  requestBody: UserRegister
}
export type TDataReadUserById = {
  user_id: string
}
export type TDataUpdateUser = {
  requestBody: UserUpdate
  user_id: string
}
export type TDataDeleteUser = {
  user_id: string
}

export class UsersService {
  /**
   * Read Users
   * Retrieve users.
   * @returns UsersPublic Successful Response
   * @throws ApiError
   */
  public static readUsers(
    data: TDataReadUsers = {},
  ): CancelablePromise<UsersPublic> {
    const { limit = 100, skip = 0 } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/users/",
      query: {
        skip,
        limit,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Create User
   * Create new user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static createUser(
    data: TDataCreateUser,
  ): CancelablePromise<UserPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/users/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read User Me
   * Get current user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static readUserMe(): CancelablePromise<UserPublic> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/users/me",
    })
  }

  /**
   * Delete User Me
   * Delete own user.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteUserMe(): CancelablePromise<Message> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/users/me",
    })
  }

  /**
   * Update User Me
   * Update own user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static updateUserMe(
    data: TDataUpdateUserMe,
  ): CancelablePromise<UserPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/v1/users/me",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update Password Me
   * Update own password.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static updatePasswordMe(
    data: TDataUpdatePasswordMe,
  ): CancelablePromise<Message> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/v1/users/me/password",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Register User
   * Create new user without the need to be logged in.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static registerUser(
    data: TDataRegisterUser,
  ): CancelablePromise<UserPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/users/signup",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read User By Id
   * Get a specific user by id.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static readUserById(
    data: TDataReadUserById,
  ): CancelablePromise<UserPublic> {
    const { user_id } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/users/{user_id}",
      path: {
        user_id: user_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update User
   * Update a user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static updateUser(
    data: TDataUpdateUser,
  ): CancelablePromise<UserPublic> {
    const { requestBody, user_id } = data
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/v1/users/{user_id}",
      path: {
        user_id: user_id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Delete User
   * Delete a user.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteUser(data: TDataDeleteUser): CancelablePromise<Message> {
    const { user_id } = data
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/users/{user_id}",
      path: {
        user_id: user_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export type TDataTestEmail = {
  emailTo: string
}

export class UtilsService {
  /**
   * Test Email
   * Test emails.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static testEmail(data: TDataTestEmail): CancelablePromise<Message> {
    const { emailTo } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/utils/test-email/",
      query: {
        email_to: emailTo,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Health Check
   * @returns boolean Successful Response
   * @throws ApiError
   */
  public static healthCheck(): CancelablePromise<boolean> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/utils/health-check/",
    })
  }
}

export type TDataReadLabs = {
  limit?: number
  skip?: number
}

export type TDataCreateLab = {
  requestBody: LabCreate
}

export type TDataReadLab = {
  lab_id: string
}

export type TDataUpdateLab = {
  lab_id: string
  requestBody: LabUpdate
}

export type TDataDeleteLab = {
  lab_id: string
}

export type TDataAddUsersToLab = {
  lab_id: string
  requestBody: AddUsersToLab
}

export type TDataViewLabUsers = {
  lab_id: string
}

export type TDataViewUserInLab = {
  lab_id: string
  user_id: string
}

export type TDataRemoveUserFromLab = {
  lab_id: string
  user_id: string
}

export type TDataUpdateUserPermissions = {
  lab_id: string
  user_id: string
  requestBody: UpdateUserLab
}

export class LabsService {
  /**
   * Read Labs
   * Retrieve labs.
   * @returns LabsPublic Successful Response
   * @throws ApiError
   */
  public static readLabs(
    data: TDataReadLabs = {},
  ): CancelablePromise<LabsPublic> {
    const { limit = 100, skip = 0 } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/labs/",
      query: {
        skip,
        limit,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Create Lab
   * Create new lab.
   * @returns LabPublic Successful Response
   * @throws ApiError
   */
  public static createLab(
    data: TDataCreateLab,
  ): CancelablePromise<LabPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/labs/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read Lab
   * Get lab by ID.
   * @returns LabPublic Successful Response
   * @throws ApiError
   */
  public static readLab(data: TDataReadLab): CancelablePromise<LabPublic> {
    const { lab_id } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/labs/{lab_id}",
      path: {
        lab_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update Lab
   * Update a lab.
   * @returns LabPublic Successful Response
   * @throws ApiError
   */
  public static updateLab(
    data: TDataUpdateLab,
  ): CancelablePromise<LabPublic> {
    const { lab_id, requestBody } = data
    return __request(OpenAPI, {
      method: "PUT",
      url: "/api/v1/labs/{lab_id}",
      path: {
        lab_id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Delete Lab
   * Delete a lab.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteLab(data: TDataDeleteLab): CancelablePromise<Message> {
    const { lab_id } = data
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/labs/{lab_id}",
      path: {
        lab_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Add Users to Lab
   * Add users to a lab by providing a list of emails and their permissions.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static addUsersToLab(
    data: TDataAddUsersToLab,
  ): CancelablePromise<Message> {
    const { lab_id, requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/labs/{lab_id}/add-users",
      path: {
        lab_id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * View Lab Users
   * View all users in a specific lab with their permissions.
   * @returns Array<User> Successful Response
   * @throws ApiError
   */
  public static viewLabUsers(
    data: TDataViewLabUsers,
  ): CancelablePromise<Array<UsersPublic>> {
    const { lab_id } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/labs/{lab_id}/users",
      path: {
        lab_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * View User in Lab
   * View a specific user in a lab.
   * @returns User Successful Response
   * @throws ApiError
   */
  public static viewUserInLab(
    data: TDataViewUserInLab,
  ): CancelablePromise<UsersPublic> {
    const { lab_id, user_id } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/labs/{lab_id}/users/{user_id}",
      path: {
        lab_id,
        user_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  // /**
  //  * Remove User from Lab
  //  * Remove a user from a lab by providing the user ID.
  //  * @returns Message Successful Response
  //  * @throws ApiError
  //  */
  // public static removeUserFromLab(
  //   data: TDataRemoveUserFromLab,
  // ): CancelablePromise<Message> {
  //   const { lab_id, user_id } = data
  //   return __request(OpenAPI, {
  //     method: "DELETE",
  //     url: "/api/v1/labs/{lab_id}/users/{user_id}/remove-user",
  //     path: {
  //       lab_id,
  //       user_id,
  //     },
  //     errors: {
  //       422: `Validation Error`,
  //     },
  //   })
  // }

  /**
   * Update User Permissions
   * Update user permissions in a lab by providing a list of user IDs and their new permissions.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static updateUserPermissions(
    data: TDataUpdateUserPermissions,
  ): CancelablePromise<Message> {
    const { lab_id, user_id, requestBody } = data
    return __request(OpenAPI, {
      method: "PUT",
      url: "/api/v1/labs/{lab_id}/users/{user_id}/update-user-permissions",
      path: {
        lab_id,
        user_id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export type TDataReadItems = {
  lab_id: string
  limit?: number
  skip?: number
}

export type TDataCreateItem = {
  lab_id: string
  requestBody: ItemCreate
}

export type TDataReadItem = {
  lab_id: string
  item_id: string
}

export type TDataUpdateItem = {
  lab_id: string
  item_id: string
  requestBody: ItemUpdate
}

export type TDataDeleteItem = {
  lab_id: string
  item_id: string
}

export class ItemsService {
  /**
   * Read Items
   * Retrieve items for a specific lab.
   * @returns ItemsPublic Successful Response
   * @throws ApiError
   */
  public static readItems(
    data: TDataReadItems,
  ): CancelablePromise<ItemsPublic> {
    const { lab_id, limit = 100, skip = 0 } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/labs/{lab_id}/items",
      path: {
        lab_id,
      },
      query: {
        skip,
        limit,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Create Item
   * Create new item for a specific lab.
   * @returns ItemPublic Successful Response
   * @throws ApiError
   */
  public static createItem(
    data: TDataCreateItem,
  ): CancelablePromise<ItemPublic> {
    const { lab_id, requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/labs/{lab_id}/items",
      path: {
        lab_id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read Item
   * Get item by ID for a specific lab.
   * @returns ItemPublic Successful Response
   * @throws ApiError
   */
  public static readItem(data: TDataReadItem): CancelablePromise<ItemPublic> {
    const { lab_id, item_id } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/labs/{lab_id}/items/{item_id}",
      path: {
        lab_id,
        item_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update Item
   * Update an item for a specific lab.
   * @returns ItemPublic Successful Response
   * @throws ApiError
   */
  public static updateItem(
    data: TDataUpdateItem,
  ): CancelablePromise<ItemPublic> {
    const { lab_id, item_id, requestBody } = data
    return __request(OpenAPI, {
      method: "PUT",
      url: "/api/v1/labs/{lab_id}/items/{item_id}",
      path: {
        lab_id,
        item_id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Delete Item
   * Delete an item for a specific lab.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteItem(data: TDataDeleteItem): CancelablePromise<Message> {
    const { lab_id, item_id } = data
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/labs/{lab_id}/items/{item_id}",
      path: {
        lab_id,
        item_id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

// export type TDataBorrowItem = {
//   lab_id: string
//   item_id: string
//   requestBody: BorrowCreate
// }

// export type TDataViewBorrowings = {
//   lab_id: string
//   item_id: string
// }

// export type TDataUpdateBorrowing = {
//   lab_id: string
//   item_id: string
//   borrow_id: string
//   requestBody: BorrowCreate
// }

// export type TDataDeleteBorrowing = {
//   lab_id: string
//   item_id: string
//   borrow_id: string
// }

// export type TDataViewBorrowing = {
//   lab_id: string
//   item_id: string
//   borrow_id: string
// }

// export class BorrowService {
//   /**
//    * Borrow Item
//    * Borrow an item from a lab by providing the start and end dates.
//    * @returns Message Successful Response
//    * @throws ApiError
//    */
//   public static borrowItem(
//     data: TDataBorrowItem,
//   ): CancelablePromise<Message> {
//     const { lab_id, item_id, requestBody } = data
//     return __request(OpenAPI, {
//       method: "POST",
//       url: "/api/v1/labs/{lab_id}/items/{item_id}/borrow",
//       path: {
//         lab_id,
//         item_id,
//       },
//       body: requestBody,
//       mediaType: "application/json",
//       errors: {
//         422: `Validation Error`,
//       },
//     })
//   }

//   /**
//    * View Borrowings
//    * View all borrowings for a specific item in a lab.
//    * @returns Array<Borrowing> Successful Response
//    * @throws ApiError
//    */
//   public static viewBorrowings(
//     data: TDataViewBorrowings,
//   ): CancelablePromise<Array<BorrowCreate>> {
//     const { lab_id, item_id } = data
//     return __request(OpenAPI, {
//       method: "GET",
//       url: "/api/v1/labs/{lab_id}/items/{item_id}/borrow",
//       path: {
//         lab_id,
//         item_id,
//       },
//       errors: {
//         422: `Validation Error`,
//       },
//     })
//   }

//   /**
//    * Update Borrowing
//    * Update the return date, table_name, and system_name of a borrowing.
//    * @returns Message Successful Response
//    * @throws ApiError
//    */
//   public static updateBorrowing(
//     data: TDataUpdateBorrowing,
//   ): CancelablePromise<Message> {
//     const { lab_id, item_id, borrow_id, requestBody } = data
//     return __request(OpenAPI, {
//       method: "PUT",
//       url: "/api/v1/labs/{lab_id}/items/{item_id}/borrow/{borrow_id}",
//       path: {
//         lab_id,
//         item_id,
//         borrow_id,
//       },
//       body: requestBody,
//       mediaType: "application/json",
//       errors: {
//         422: `Validation Error`,
//       },
//     })
//   }

//   /**
//    * Delete Borrowing
//    * Delete a borrowing.
//    * @returns Message Successful Response
//    * @throws ApiError
//    */
//   public static deleteBorrowing(
//     data: TDataDeleteBorrowing,
//   ): CancelablePromise<Message> {
//     const { lab_id, item_id, borrow_id } = data
//     return __request(OpenAPI, {
//       method: "DELETE",
//       url: "/api/v1/labs/{lab_id}/items/{item_id}/borrow/{borrow_id}",
//       path: {
//         lab_id,
//         item_id,
//         borrow_id,
//       },
//       errors: {
//         422: `Validation Error`,
//       },
//     })
//   }

//   /**
//    * View Borrowing
//    * View details of a specific borrowing.
//    * @returns Borrowing Successful Response
//    * @throws ApiError
//    */
//   public static viewBorrowing(
//     data: TDataViewBorrowing,
//   ): CancelablePromise<BorrowCreate> {
//     const { lab_id, item_id, borrow_id } = data
//     return __request(OpenAPI, {
//       method: "GET",
//       url: "/api/v1/labs/{lab_id}/items/{item_id}/borrow/{borrow_id}",
//       path: {
//         lab_id,
//         item_id,
//         borrow_id,
//       },
//       errors: {
//         422: `Validation Error`,
//       },
//     })
//   }
// }