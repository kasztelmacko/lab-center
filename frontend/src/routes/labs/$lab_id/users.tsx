import {
  Container,
  SkeletonText,
  Card,
  CardHeader,
  CardBody,
  Text,
  SimpleGrid,
  Icon,
} from "@chakra-ui/react"
import { FiMail, FiUser } from "react-icons/fi"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { z } from "zod"

import { LabsService, UserLabPublic } from "../../../client"
import Navbar from "../../../components/Common/Navbar"
import AddUserLab from "../../../components/UserLabs/AddUserLab"

const UsersLabSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/$lab_id/users")({
  component: UserLabs,
  validateSearch: (search) => UsersLabSearchSchema.parse(search),
})

function getUserLabsQueryOptions(lab_id: string) {
  return {
    queryFn: () => {
      return LabsService.viewLabUsers({ lab_id })
    },
    queryKey: ["labs", lab_id],
  }
}

function UserLabsCards() {
  const { lab_id } = Route.useParams()
  const {
    data: users,
    isPending: isUserLabsPending,
    isPlaceholderData: isUserLabsPlaceholderData,
  } = useQuery({
    ...getUserLabsQueryOptions(lab_id),
    placeholderData: (prevData) => prevData,
  })

  return (
    <>
      <SimpleGrid columns={{ base: 1, md: 3, lg: 4 }} spacing={4}>
        {isUserLabsPending ? (
          new Array(5).fill(null).map((_, index) => (
            <Card key={index} opacity={isUserLabsPlaceholderData ? 0.5 : 1}>
              <CardHeader>
                <SkeletonText noOfLines={1} />
              </CardHeader>
              <CardBody>
                <SkeletonText noOfLines={3} />
              </CardBody>
            </Card>
          ))
        ) : (
          Array.isArray(users) && users.map((user: UserLabPublic) => (
            <UserLabCard key={user.user_id} user={user} />
          ))
        )}
      </SimpleGrid>
    </>
  )
}

function UserLabCard({ user }: { user: UserLabPublic }) {
  return (
    <Card>
      <CardHeader>
        <Text>
          <Icon as={FiUser} mr={2} />
          owner: {user.full_name}
        </Text>
        <Text>
          <Icon as={FiMail} mr={2} />
          contact: {user.email}
        </Text>
      </CardHeader>
      <CardBody>
        <Text>{user.can_edit_lab ? 'Can Edit Lab' : 'Cannot Edit Lab'}</Text>
        <Text>{user.can_edit_items ? 'Can Edit Items' : 'Cannot Edit Items'}</Text>
        <Text>{user.can_edit_users ? 'Can Edit Users' : 'Cannot Edit Users'}</Text>
      </CardBody>
    </Card>
  )
}

function UserLabs() {
  return (
    <Container maxW="full">
      <Navbar type={"users"} addModalAs={AddUserLab} />
      <UserLabsCards />
    </Container>
  )
}