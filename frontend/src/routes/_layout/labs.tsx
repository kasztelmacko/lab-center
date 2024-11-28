import {
  Container,
  Heading,
  SkeletonText,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Text,
  SimpleGrid,
  Center,
  Icon,
  Button,
} from "@chakra-ui/react"
import { FiMapPin, FiMail, FiUser } from "react-icons/fi"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute, Link } from "@tanstack/react-router"
import { z } from "zod"

import { LabsService, UsersService, LabPublic } from "../../client"
import Navbar from "../../components/Common/Navbar"
import AddLab from "../../components/Labs/AddLab"

const labsSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/labs")({
  component: Labs,
  validateSearch: (search) => labsSearchSchema.parse(search),
})

function getLabsQueryOptions() {
  return {
    queryFn: () => LabsService.readLabs(),
    queryKey: ["labs"],
  }
}

function getUserQueryOptions({ owner_id }: { owner_id: string }) {
  return {
    queryFn: () => UsersService.readUserById({ user_id: owner_id }),
    queryKey: ["user", { owner_id }],
  }
}

function LabsCards() {
  const {
    data: labs,
    isPending: isLabsPending,
    isPlaceholderData: isLabsPlaceholderData,
  } = useQuery({
    ...getLabsQueryOptions(),
    placeholderData: (prevData) => prevData,
  })

  return (
    <>
      <SimpleGrid columns={{ base: 1, md: 3, lg: 4 }} spacing={4}>
        {isLabsPending ? (
          new Array(5).fill(null).map((_, index) => (
            <Card key={index} opacity={isLabsPlaceholderData ? 0.5 : 1}>
              <CardHeader>
                <SkeletonText noOfLines={1} />
              </CardHeader>
              <CardBody>
                <SkeletonText noOfLines={3} />
              </CardBody>
            </Card>
          ))
        ) : (
          labs?.data.map((lab: LabPublic) => (
            <LabCard key={lab.lab_id} lab={lab} />
          ))
        )}
      </SimpleGrid>
    </>
  )
}

function LabCard({ lab }: { lab: LabPublic }) {
  const {
    data: user,
    isPending: isUserPending,
    isPlaceholderData: isUserPlaceholderData,
  } = useQuery({
    ...getUserQueryOptions({ owner_id: lab.owner_id }),
    placeholderData: (prevData) => prevData,
  })

  return (
    <Card opacity={isUserPlaceholderData ? 0.5 : 1}>
      <CardHeader>
        <Center>
          <Heading size="4xl">{lab.lab_place}</Heading>
        </Center>
      </CardHeader>
      <CardBody>
        <Center>
          <Icon as={FiMapPin} mr={2} />
          <Text>{lab.lab_university} | {lab.lab_num}</Text>
        </Center>
        {isUserPending ? (
          <SkeletonText noOfLines={2} />
        ) : (
          <>
            <Text><br></br></Text>
            <Text>
              <Icon as={FiUser} mr={2} />
              owner: {user?.full_name}
            </Text>
            <Text>
              <Icon as={FiMail} mr={2} />
              contact: {user?.email}
            </Text>
          </>
        )}
      </CardBody>
      <CardFooter>
        <Center>
          <SimpleGrid columns={2} spacing="4">
            <Button
              width="100%"
              variant="primary"
              py={2}
              my={1}
            >
              Items
            </Button>
            <Link
              to={`/labs/${lab.lab_id}/users`}
              style={{ width: '100%' }}
            >
              <Button
                width="100%"
                variant="primary"
                py={2}
                my={1}
              >
                Users
              </Button>
            </Link>
          </SimpleGrid>
        </Center>
      </CardFooter>
    </Card>
  )
}

function Labs() {
  return (
    <Container maxW="full">
      <Navbar type={"lab"} addModalAs={AddLab} />
      <LabsCards />
    </Container>
  )
}