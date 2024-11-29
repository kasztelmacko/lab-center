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

import { type ApiError, type LabCreate, LabsService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

interface AddLabProps {
  isOpen: boolean
  onClose: () => void
}

const AddLab = ({ isOpen, onClose }: AddLabProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<LabCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      lab_place: "",
      lab_university: "",
      lab_num: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: LabCreate) =>
      LabsService.createLab({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Lab created successfully.", "success")
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["labs"] })
    },
  })

  const onSubmit: SubmitHandler<LabCreate> = (data) => {
    mutation.mutate(data)
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
          <ModalHeader>Add Lab</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.lab_place}>
              <FormLabel htmlFor="title">Place</FormLabel>
              <Input
                id="lab_place"
                {...register("lab_place", {
                  required: "Place is required.",
                })}
                placeholder="ex. IMiF"
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
                placeholder="ex. University of Warsaw"
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
                placeholder="ex. B4.01"
                type="text"
              />
              {errors.lab_num && (
                <FormErrorMessage>{errors.lab_num.message}</FormErrorMessage>
              )}
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
    </>
  )
}

export default AddLab;
