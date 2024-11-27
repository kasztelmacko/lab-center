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
  
  import { LabsService } from "../../client"
  import ActionsMenu from "../../components/Common/ActionsMenu"
  import Navbar from "../../components/Common/Navbar"
  import AddLab from "../../components/Labs/AddLab"
  import { PaginationFooter } from "../../components/Common/PaginationFooter.tsx"
  
  const labsSearchSchema = z.object({
    page: z.number().catch(1),
  })
  
  export const Route = createFileRoute("/_layout/labs")({
    component: Labs,
    validateSearch: (search) => labsSearchSchema.parse(search),
  })
  
  const PER_PAGE = 5
  
  function getLabsQueryOptions({ page }: { page: number }) {
    return {
      queryFn: () =>
        LabsService.readLabs({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
      queryKey: ["labs", { page }],
    }
  }
  
  function LabsTable() {
    const queryClient = useQueryClient()
    const { page } = Route.useSearch()
    const navigate = useNavigate({ from: Route.fullPath })
    const setPage = (page: number) =>
      navigate({ search: (prev: {[key: string]: string}) => ({ ...prev, page }) })
  
    const {
      data: labs,
      isPending,
      isPlaceholderData,
    } = useQuery({
      ...getLabsQueryOptions({ page }),
      placeholderData: (prevData) => prevData,
    })
  
    const hasNextPage = !isPlaceholderData && labs?.data.length === PER_PAGE
    const hasPreviousPage = page > 1
  
    useEffect(() => {
      if (hasNextPage) {
        queryClient.prefetchQuery(getLabsQueryOptions({ page: page + 1 }))
      }
    }, [page, queryClient, hasNextPage])
  
    return (
      <>
        <TableContainer>
          <Table size={{ base: "sm", md: "md" }}>
            <Thead>
              <Tr>
                <Th>ID</Th>
                <Th>Lab Place</Th>
                <Th>Lab University</Th>
                <Th>Lab Number</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            {isPending ? (
              <Tbody>
                <Tr>
                  {new Array(4).fill(null).map((_, index) => (
                    <Td key={index}>
                      <SkeletonText noOfLines={1} paddingBlock="16px" />
                    </Td>
                  ))}
                </Tr>
              </Tbody>
            ) : (
              <Tbody>
                {labs?.data.map((lab) => (
                  <Tr key={lab.lab_id} opacity={isPlaceholderData ? 0.5 : 1}>
                    <Td>{lab.lab_id}</Td>
                    <Td isTruncated maxWidth="150px">
                      {lab.lab_place}
                    </Td>
                    <Td isTruncated maxWidth="150px">
                      {lab.lab_university}
                    </Td>
                    <Td isTruncated maxWidth="150px">
                      {lab.lab_num}
                    </Td>
                    <Td>
                      <ActionsMenu type={"Lab"} value={lab} />
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
  
  function Labs() {
    return (
      <Container maxW="full">
        <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
          Labs Management
        </Heading>
  
        <Navbar type={"lab"} addModalAs={AddLab} />
        <LabsTable />
      </Container>
    )
  }
  