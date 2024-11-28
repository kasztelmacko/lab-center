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
  import { createRoute, useParams } from "@tanstack/react-router"
  import { Route as LabsRoute } from "../../routes/_layout/labs";
  import { z } from "zod"
  
  import { LabsService, UsersService, UserLab, UserLabPublic } from "../../client"
  import Navbar from "../../components/Common/Navbar"
  import AddUserLab from "../../components/UserLabs/AddUserLab"
  
  const UsersLabSearchSchema = z.object({
    page: z.number().catch(1),
  })
  
  export const Route = createRoute({
    path: "/:lab_id/users",
    component: UserLabs,
    validateSearch: (search) => UsersLabSearchSchema.parse(search),
    getParentRoute: () => LabsRoute,
  });
  
  function getUserLabsQueryOptions() {
    const { lab_id } = useParams({ from: Route });
    return {
      queryFn: () => LabsService.viewLabUsers(lab_id),
      queryKey: ["labs", lab_id],
    }
  }

  function getUserQueryOptions({ user_id }: { user_id: string }) {
    return {
      queryFn: () => UsersService.readUserById({ user_id: user_id }),
      queryKey: ["user", { user_id }],
    }
  }
  
  function UserLabsCards() {
    const {
      data: userlabs,
      isPending: isUserLabsPending,
      isPlaceholderData: isUserLabsPlaceholderData,
    } = useQuery({
      ...getUserLabsQueryOptions(),
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
            userlabs?.data.map((userlab: UserLabPublic) => (
              <UserLabCard key={userlab.user_id} userlab={userlab} />
            ))
          )}
        </SimpleGrid>
      </>
    )
  }
  
  function UserLabCard({ userlab }: { userlab: UserLab }) {
    const {
        data: user,
        isPending: isUserPending,
        isPlaceholderData: isUserPlaceholderData,
    } = useQuery({
        ...getUserQueryOptions({ user_id: userlab.user_id }),
        placeholderData: (prevData) => prevData,
    })

    return (
        <Card opacity={isUserPlaceholderData ? 0.5 : 1}>
            <CardHeader>
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
            </CardHeader>
            <CardBody>
                <Text>{userlab.can_edit_lab}</Text>
                <Text>{userlab.can_edit_items}</Text>
                <Text>{userlab.can_edit_users}</Text>
            </CardBody>
        </Card>
    )
}
  
  function UserLabs() {
    return (
      <Container maxW="full">
  
        <Navbar type={"userlab"} addModalAs={AddUserLab} />
        <UserLabsCards />
      </Container>
    )
  }