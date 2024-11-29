import {
    Button,
    FormControl,
    FormLabel,
    Checkbox,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
  } from "@chakra-ui/react"
  import { useMutation, useQueryClient } from "@tanstack/react-query"
  import { type SubmitHandler, useForm } from "react-hook-form"
  
  import {
    type ApiError,
    type UpdateUserLab,
    LabsService,
    UserLab,
  } from "../../client"
  import useCustomToast from "../../hooks/useCustomToast"
  import { handleError } from "../../utils"
  
  interface UpdateUserLabProps {
    userlab: UserLab
    isOpen: boolean
    onClose: () => void
    initialPermissions: UpdateUserLab
  }
  
  const UpdateUserLab = ({ userlab, isOpen, onClose, initialPermissions }: UpdateUserLabProps) => {
    const queryClient = useQueryClient()
    const showToast = useCustomToast()
    const {
      register,
      handleSubmit,
      reset,
      formState: { isSubmitting, errors, isDirty },
    } = useForm<UpdateUserLab>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: initialPermissions,
    })
  
    const mutation = useMutation({
      mutationFn: (data: UpdateUserLab) =>
        LabsService.updateUserPermissions({ lab_id: userlab.lab_id, user_id: userlab.user_id, requestBody: data }),
      onSuccess: () => {
        showToast("Success!", "User permissions updated successfully.", "success")
        onClose()
      },
      onError: (err: ApiError) => {
        handleError(err, showToast)
      },
      onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ["labs"] })
      },
    })
  
    const onSubmit: SubmitHandler<UpdateUserLab> = async (data) => {
      mutation.mutate(data)
    }
  
    const onCancel = () => {
      reset()
      onClose()
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
          <ModalHeader>Update User Permissions</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl mt={4} isInvalid={!!errors.can_edit_lab}>
              <FormLabel htmlFor="can_edit_lab">Can Edit Lab</FormLabel>
              <Checkbox
                id="can_edit_lab"
                {...register("can_edit_lab")}
              />
            </FormControl>
  
            <FormControl mt={4} isInvalid={!!errors.can_edit_items}>
              <FormLabel htmlFor="can_edit_items">Can Edit Items</FormLabel>
              <Checkbox
                id="can_edit_items"
                {...register("can_edit_items")}
              />
            </FormControl>
  
            <FormControl mt={4} isInvalid={!!errors.can_edit_users}>
              <FormLabel htmlFor="can_edit_users">Can Edit Users</FormLabel>
              <Checkbox
                id="can_edit_users"
                {...register("can_edit_users")}
              />
            </FormControl>
          </ModalBody>
          <ModalFooter gap={3}>
            <Button
              variant="primary"
              type="submit"
              isLoading={isSubmitting}
              isDisabled={!isDirty}
            >
              Save
            </Button>
            <Button onClick={onCancel}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    )
  }
  
  export default UpdateUserLab