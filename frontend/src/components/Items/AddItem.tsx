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

import { type ApiError, type ItemCreate, ItemsService, TDataCreateItem } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

interface AddItemProps {
  isOpen: boolean
  onClose: () => void
  labId: string // Pass the lab_id from the parent component
}

const AddItem = ({ isOpen, onClose, labId }: AddItemProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ItemCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      item_name: "",
      quantity: undefined,
      item_img_url: undefined,
      item_vendor: undefined,
      item_params: undefined,
      lab_id: labId, // Set the lab_id from the parent component
    },
  })

  const mutation = useMutation({
    mutationFn: (data: ItemCreate) =>
      ItemsService.createItem({ lab_id: labId, requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Item created successfully.", "success")
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] })
    },
  })

  const onSubmit: SubmitHandler<ItemCreate> = (data) => {
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
          <ModalHeader>Add Item</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.item_name}>
              <FormLabel htmlFor="item_name">Item Name</FormLabel>
              <Input
                id="item_name"
                {...register("item_name", {
                  required: "Item Name is required.",
                })}
                placeholder="Item Name"
                type="text"
              />
              {errors.item_name && (
                <FormErrorMessage>{errors.item_name.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4} isInvalid={!!errors.quantity}>
              <FormLabel htmlFor="quantity">Quantity</FormLabel>
              <Input
                id="quantity"
                {...register("quantity", {
                  valueAsNumber: true,
                  validate: (value) =>
                    value === undefined || value >= 0 || "Quantity must be a non-negative number.",
                })}
                placeholder="Quantity"
                type="number"
              />
              {errors.quantity && (
                <FormErrorMessage>{errors.quantity.message}</FormErrorMessage>
              )}
            </FormControl>

            <FormControl mt={4}>
              <FormLabel htmlFor="item_img_url">Item Image URL</FormLabel>
              <Input
                id="item_img_url"
                {...register("item_img_url")}
                placeholder="Item Image URL"
                type="text"
              />
            </FormControl>

            <FormControl mt={4}>
              <FormLabel htmlFor="item_vendor">Item Vendor</FormLabel>
              <Input
                id="item_vendor"
                {...register("item_vendor")}
                placeholder="Item Vendor"
                type="text"
              />
            </FormControl>

            <FormControl mt={4}>
              <FormLabel htmlFor="item_params">Item Parameters</FormLabel>
              <Input
                id="item_params"
                {...register("item_params")}
                placeholder="Item Parameters"
                type="text"
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
    </>
  )
}

export default AddItem