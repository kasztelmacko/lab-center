import {
  Container,
  Heading,
  SkeletonText,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useEffect } from "react"
import { z } from "zod"

import { ItemsService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"
import AddItem from "../../components/Items/AddItem"
import { PaginationFooter } from "../../components/Common/PaginationFooter.tsx"

const itemsSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/items")({
  component: Items,
  validateSearch: (search) => itemsSearchSchema.parse(search),
})

const PER_PAGE = 5

function getItemsQueryOptions({ page, lab_id }: { page: number; lab_id: string }) {
  return {
    queryFn: () =>
      ItemsService.readItems({ lab_id, skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["items", { page, lab_id }],
  }
}

interface ItemsTableProps {
  lab_id: string;
}

function ItemsTable({ lab_id }: ItemsTableProps) {
  const queryClient = useQueryClient()
  const { page } = Route.useSearch()
  const navigate = useNavigate({ from: Route.fullPath })
  const setPage = (page: number) =>
    navigate({ search: (prev: {[key: string]: string}) => ({ ...prev, page }) })

  const {
    data: items,
    isPending,
    isPlaceholderData,
  } = useQuery({
    ...getItemsQueryOptions({ page, lab_id }),
    placeholderData: (prevData) => prevData,
  })

  const hasNextPage = !isPlaceholderData && items?.data.length === PER_PAGE
  const hasPreviousPage = page > 1

  useEffect(() => {
    if (hasNextPage) {
      queryClient.prefetchQuery(getItemsQueryOptions({ page: page + 1, lab_id }))
    }
  }, [page, queryClient, hasNextPage, lab_id])

  return (
    <>
      <TableContainer>
        <Table size={{ base: "sm", md: "md" }}>
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Item Name</Th>
              <Th>Quantity</Th>
              <Th>Item Image URL</Th>
              <Th>Item Vendor</Th>
              <Th>Item Parameters</Th>
              <Th>Lab ID</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          {isPending ? (
            <Tbody>
              <Tr>
                {new Array(8).fill(null).map((_, index) => (
                  <Td key={index}>
                    <SkeletonText noOfLines={1} paddingBlock="16px" />
                  </Td>
                ))}
              </Tr>
            </Tbody>
          ) : (
            <Tbody>
              {items?.data.map((item) => (
                <Tr key={item.item_id} opacity={isPlaceholderData ? 0.5 : 1}>
                  <Td>{item.item_id}</Td>
                  <Td isTruncated maxWidth="150px">
                    {item.item_name}
                  </Td>
                  <Td>{item.quantity || "N/A"}</Td>
                  <Td isTruncated maxWidth="150px">
                    {item.item_img_url || "N/A"}
                  </Td>
                  <Td isTruncated maxWidth="150px">
                    {item.item_vendor || "N/A"}
                  </Td>
                  <Td isTruncated maxWidth="150px">
                    {item.item_params || "N/A"}
                  </Td>
                  <Td>{item.lab_id}</Td>
                  <Td>
                    <ActionsMenu type={"Item"} value={item} />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          )}
        </Table>
      </TableContainer>
      <PaginationFooter
        page={page}
        onChangePage={setPage}
        hasNextPage={hasNextPage}
        hasPreviousPage={hasPreviousPage}
      />
    </>
  )
}

function Items({ lab_id }: { lab_id: string }) {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Items Management
      </Heading>

      <Navbar type={"Item"} addModalAs={AddItem} />
      <ItemsTable lab_id={lab_id} />
    </Container>
  )
}