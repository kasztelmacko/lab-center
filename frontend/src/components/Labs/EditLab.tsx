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
  } from "@chakra-ui/react"
  import { useMutation, useQueryClient } from "@tanstack/react-query"
  import { type SubmitHandler, useForm } from "react-hook-form"
  
  import {
    type ApiError,
    type LabPublic,
    type LabUpdate,
    LabsService,
  } from "../../client"
  import useCustomToast from "../../hooks/useCustomToast"
  import { handleError } from "../../utils"
  
  interface EditLabProps {
    lab: LabPublic
    isOpen: boolean
    onClose: () => void
  }
  
  const EditLab = ({ lab, isOpen, onClose }: EditLabProps) => {
    const queryClient = useQueryClient()
    const showToast = useCustomToast()
    const {
      register,
      handleSubmit,
      reset,
      formState: { isSubmitting, errors, isDirty },
    } = useForm<LabUpdate>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: lab,
    })
  
    const mutation = useMutation({
      mutationFn: (data: LabPublic) =>
        LabsService.updateLab({ lab_id: lab.lab_id, requestBody: data }),
      onSuccess: () => {
        showToast("Success!", "Lab updated successfully.", "success")
        onClose()
      },
      onError: (err: ApiError) => {
        handleError(err, showToast)
      },
      onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ["labs"] })
      },
    })
  
    const onSubmit: SubmitHandler<LabUpdate> = async (data) => {
      mutation.mutate(data)
    }
  
    const onCancel = () => {
      reset()
      onClose()
    }
  
    return (
      <>
        <Modal
          isOpen={isOpen}
          onClose={onClose}
          size={{ base: "sm", md: "md" }}
          isCentered
        >
          <ModalOverlay />
          <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
            <ModalHeader>Edit Lab</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <FormControl isRequired isInvalid={!!errors.lab_place}>
                <FormLabel htmlFor="title">Place</FormLabel>
                <Input
                  id="lab_place"
                  {...register("lab_place", {
                    required: "Place is required.",
                  })}
                  placeholder="Place"
                  type="text"
                />
                {errors.lab_place && (
                  <FormErrorMessage>{errors.lab_place.message}</FormErrorMessage>
                )}
              </FormControl>
              <FormControl mt={4}>
                <FormLabel htmlFor="lab_university">University</FormLabel>
                <Input
                  id="lab_university"
                  {...register("lab_university")}
                  placeholder="University"
                  type="text"
                />
                {errors.lab_university && (
                  <FormErrorMessage>{errors.lab_university.message}</FormErrorMessage>
                )}
              </FormControl>
              <FormControl mt={4}>
                <FormLabel htmlFor="lab_num">University</FormLabel>
                <Input
                  id="lab_num"
                  {...register("lab_num")}
                  placeholder="Number"
                  type="text"
                />
                {errors.lab_num && (
                  <FormErrorMessage>{errors.lab_num.message}</FormErrorMessage>
                )}
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
      </>
    )
  }
  
  export default EditLab
  