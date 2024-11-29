import {
  Container,
  SkeletonText,
  Card,
  CardHeader,
  CardBody,
  Text,
  SimpleGrid,
  Icon,
  Center,
  Heading,
} from "@chakra-ui/react"
import { FiMail } from "react-icons/fi"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { z } from "zod"

import { LabsService, UserLabPublic } from "../../../client"
import Navbar from "../../../components/Common/Navbar"
import AddUserLab from "../../../components/UserLabs/AddUserLab"
import ActionsMenu from "../../../components/Common/ActionsMenu"

const UsersLabSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/labs/$lab_id/users")({
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
      <SimpleGrid columns={{ base: 1, md: 3, lg: 5 }} spacing={4}>
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
        <Center>
          <Text>
            <Heading size="2xl">{user.full_name}</Heading>
          </Text>
        </Center>
      </CardHeader>
      <CardBody>
        <Center>
          <Text>
            <Icon as={FiMail} mr={2} />
            contact: {user.email}
          </Text>
        </Center>
        {user.can_edit_users && <ActionsMenu type={"UserLab"} value={user} />}
      </CardBody>
    </Card>
  );
}

function UserLabs() {
  const { lab_id } = Route.useParams()
  return (
    <Container maxW="full">
      <Navbar type={"users"} addModalAs={AddUserLab} labId={lab_id}/>
      <UserLabsCards />
    </Container>
  )
}