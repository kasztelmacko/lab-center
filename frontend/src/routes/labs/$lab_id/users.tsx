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
} from "@chakra-ui/react";
import { FiMail } from "react-icons/fi";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";

import { LabsService, UserLabPublic, UserPublic } from "../../../client";
import Navbar from "../../../components/Common/Navbar";
import AddUserLab from "../../../components/UserLabs/AddUserLab";
import ActionsMenu from "../../../components/Common/ActionsMenu";
import useAuth from "../../../hooks/useAuth";

const UsersLabSearchSchema = z.object({
  page: z.number().catch(1),
});

export const Route = createFileRoute("/labs/$lab_id/users")({
  component: UserLabs,
  validateSearch: (search) => UsersLabSearchSchema.parse(search),
});

function getUserLabsQueryOptions(lab_id: string) {
  return {
    queryFn: () => {
      return LabsService.viewLabUsers({ lab_id });
    },
    queryKey: ["labs", lab_id],
  };
}

function getCurrentUserPermissions(user_id: string, lab_id: string) {
  return {
    queryFn: () => {
      return LabsService.viewLabUser({ user_id, lab_id });
    },
    queryKey: ["labs", lab_id, "users", user_id],
  };
}

interface UserLabsCardsProps {
  currentUser: UserPublic;
}

function UserLabsCards({ currentUser }: UserLabsCardsProps) {
  const { lab_id } = Route.useParams();
  const {
    data: users,
    isPending: isUserLabsPending,
    isPlaceholderData: isUserLabsPlaceholderData,
  } = useQuery({
    ...getUserLabsQueryOptions(lab_id),
    placeholderData: (prevData) => prevData,
  });

  return (
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
        Array.isArray(users) &&
        users.map((user: UserLabPublic) => (
          <UserLabCard key={user.user_id} user={user} currentUser={currentUser} />
        ))
      )}
    </SimpleGrid>
  );
}

interface UserLabCardProps {
  user: UserLabPublic;
  currentUser: UserPublic;
}

function UserLabCard({ user, currentUser }: UserLabCardProps) {
  const { lab_id } = Route.useParams();
  const { 
    data: currentUserPermissions, 
    isLoading: isLoadingPermissions, 
    error: permissionsError 
  } = useQuery(
    getCurrentUserPermissions(currentUser.user_id, lab_id)
  );

  console.log(currentUserPermissions);

  if (isLoadingPermissions) {
    return (
      <Card>
        <CardHeader>
          <SkeletonText noOfLines={1} />
        </CardHeader>
        <CardBody>
          <SkeletonText noOfLines={3} />
        </CardBody>
      </Card>
    );
  }

  if (permissionsError || !currentUserPermissions) {
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
        </CardBody>
      </Card>
    );
  }

  const canEdit = currentUserPermissions.can_edit_users;

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
        {canEdit && <ActionsMenu type={"UserLab"} value={user} />}
      </CardBody>
    </Card>
  );
}

function UserLabs() {
  const { user: currentUser } = useAuth();
  if (!currentUser) {
    return null;
  }
  const { lab_id } = Route.useParams();
  return (
    <Container maxW="full">
      <Navbar type={"users"} addModalAs={AddUserLab} labId={lab_id} />
      <UserLabsCards currentUser={currentUser} />
    </Container>
  );
}

export default UserLabs;
