"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiClient } from "@/lib/api-client";
import type { AuthProviderLink, UserPreferences, UserProfile } from "@/types";

export function useProfile() {
  return useQuery({
    queryKey: ["profile"],
    queryFn: () => apiClient.get<UserProfile>("/users/me"),
  });
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (updates: Partial<UserProfile>) =>
      apiClient.patch<UserProfile>("/users/me", updates),
    onSuccess: (data) => {
      queryClient.setQueryData(["profile"], data);
    },
  });
}

export function usePreferences() {
  return useQuery({
    queryKey: ["preferences"],
    queryFn: () => apiClient.get<UserPreferences>("/users/me/preferences"),
  });
}

export function useUpdatePreferences() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (updates: Partial<UserPreferences>) =>
      apiClient.patch<UserPreferences>("/users/me/preferences", updates),
    onSuccess: (data) => {
      queryClient.setQueryData(["preferences"], data);
    },
  });
}

export function useAuthProviders() {
  return useQuery({
    queryKey: ["auth-providers"],
    queryFn: () => apiClient.get<AuthProviderLink[]>("/users/me/auth-providers"),
  });
}
