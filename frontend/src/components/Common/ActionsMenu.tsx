import {
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  useDisclosure,
} from "@chakra-ui/react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiTrash } from "react-icons/fi";

import type { ItemPublic, LabPublic, UserPublic } from "../../client";
import EditUser from "../Admin/EditUser";
import EditItem from "../Items/EditItem";
import EditLab from "../Labs/EditLab";
import Delete from "./DeleteAlert";

interface ActionsMenuProps {
  type: string;
  value: ItemPublic | UserPublic | LabPublic;
  disabled?: boolean;
}

const ActionsMenu = ({ type, value, disabled }: ActionsMenuProps) => {
  const editUserModal = useDisclosure();
  const deleteModal = useDisclosure();

  const getId = (value: UserPublic | ItemPublic | LabPublic) => {
    if (type === "User") {
      return { user_id: (value as UserPublic).user_id };
    } else if (type === "Item") {
      return {
        lab_id: (value as ItemPublic).lab_id,
        item_id: (value as ItemPublic).item_id,
      };
    } else if (type === "Lab") {
      return { lab_id: (value as LabPublic).lab_id };
    }
    return {};
  };

  const ids = getId(value);

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          <MenuItem
            onClick={editUserModal.onOpen}
            icon={<FiEdit fontSize="16px" />}
          >
            Edit {type}
          </MenuItem>
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {type === "User" ? (
          <EditUser
            user={value as UserPublic}
            isOpen={editUserModal.isOpen}
            onClose={editUserModal.onClose}
          />
        ) : type === "Item" ? (
          <EditItem
            item={value as ItemPublic}
            isOpen={editUserModal.isOpen}
            onClose={editUserModal.onClose}
          />
        ) : type === "Lab" ? (
          <EditLab
            lab={value as LabPublic}
            isOpen={editUserModal.isOpen}
            onClose={editUserModal.onClose}
          />
        ) : null}
        <Delete
          type={type}
          user_id={ids.user_id}
          lab_id={ids.lab_id}
          item_id={ids.item_id}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
        />
      </Menu>
    </>
  );
};

export default ActionsMenu;
