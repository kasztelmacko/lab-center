import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Checkbox,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import { type ApiError, type AddUsersToLab, LabsService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

interface AddUserLabProps {
  isOpen: boolean
  onClose: () => void
  labId: string
  
}

const AddUserLab = ({ isOpen, onClose, labId }: AddUserLabProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
      register,
      handleSubmit,
      reset,
      formState: { errors, isSubmitting },
  } = useForm<AddUsersToLab>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: {
          email: "",
          can_edit_items: false,
          can_edit_lab: false,
          can_edit_users: false,
      },
  })

  const mutation = useMutation({
    mutationFn: (data: AddUsersToLab) => {
        return LabsService.addUsersToLab({ lab_id: labId, requestBody: data });
    },
    onSuccess: () => {
        showToast("Success!", "User added to Lab successfully.", "success");
        reset();
        onClose();
    },
    onError: (err: ApiError) => {
        handleError(err, showToast);
    },
    onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ["labs"] });
    },
});

  const onSubmit: SubmitHandler<AddUsersToLab> = (data) => {
      mutation.mutate(data)
  }

  return (
      <Modal
          isOpen={isOpen}
          onClose={onClose}
          size={{ base: "sm", md: "md" }}
          isCentered
      >
          <ModalOverlay />
          <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
              <ModalHeader>Add User to Lab</ModalHeader>
              <ModalCloseButton />
              <ModalBody pb={6}>
                  <FormControl isRequired isInvalid={!!errors.email}>
                      <FormLabel htmlFor="email">Email</FormLabel>
                      <Input
                          id="email"
                          {...register("email", {
                              required: "Email is required.",
                          })}
                          placeholder="Enter email"
                          type="email"
                      />
                      {errors.email && (
                          <FormErrorMessage>{errors.email.message}</FormErrorMessage>
                      )}
                  </FormControl>
                  <FormControl mt={4}>
                      <FormLabel htmlFor="can_edit_lab">Can Edit Lab</FormLabel>
                      <Checkbox
                          id="can_edit_lab"
                          {...register("can_edit_lab")}
                      />
                  </FormControl>
                  <FormControl mt={4}>
                      <FormLabel htmlFor="can_edit_items">Can Edit Items</FormLabel>
                      <Checkbox
                          id="can_edit_items"
                          {...register("can_edit_items")}
                      />
                  </FormControl>
                  <FormControl mt={4}>
                      <FormLabel htmlFor="can_edit_users">Can Edit Users</FormLabel>
                      <Checkbox
                          id="can_edit_users"
                          {...register("can_edit_users")}
                      />
                  </FormControl>
              </ModalBody>

              <ModalFooter gap={3}>
                  <Button variant="primary" type="submit" isLoading={isSubmitting}>
                      Save
                  </Button>
                  <Button onClick={onClose}>Cancel</Button>
              </ModalFooter>
          </ModalContent>
      </Modal>
  )
}

export default AddUserLab
