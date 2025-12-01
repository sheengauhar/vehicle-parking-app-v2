import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      beforeEnter: () => {
        const auth = useAuthStore();
        if (auth.isAuthenticated) {
          if (auth.getUserRoles().includes("admin")) {
            return "/admin/dashboard";
          }
          if (auth.getUserRoles().includes("user")) {
            return "/user/dashboard";
          }
        }
      }
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },

    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, adminOnly: true }
    },

    {
      path: '/admin/parking_lots/:id/edit',
      name: 'edit-parking-lot',
      component: () => import('@/views/EditParkingLot.vue'),
      meta: { requiresAuth: true, adminOnly: true }
    },

    {
      path: '/add-lot',
      name: 'addLot',
      component: () => import('@/views/AddParkingLot.vue'),
      meta: { requiresAuth: true, adminOnly: true } 
    },

    {
      path: "/admin/users",
      name: "AdminUsers",
      component: () => import("../views/AdminUsers.vue"),
      meta: { requiresAuth: true, adminOnly: true } 
    },

    {
      path: "/admin/summary",
      name: 'AdminSummary',
      component: () => import("@/views/AdminSummary.vue"),
      meta: { requiresAuth: true, adminOnly: true } 
    },

    // users    
    {
      path: '/user/dashboard',
      name: 'UserDashboard',
      component: () => import('@/views/UserDashboard.vue'),
      meta: { requiresAuth: true }
    },

    { 
      path: '/book-spots', 
      component: () => import('@/views/BookSpots.vue'),
      meta: { requiresAuth: true, adminOnly: true } 
    },

    { 
      path: '/confirm-booking/:lot_id', 
      name: 'ConfirmBooking',
      component: () => import('@/views/ConfirmBooking.vue'), 
      props: true,
      meta: { requiresAuth: true }
     },

    {
      path: "/user/summary/usage_per_lot",
      name: "UserSummary",
      component: () => import("@/views/UserSummary.vue"),
      meta: { requiresAuth: true }
    },

    {
      path: "/edit-profile",
      name: "EditProfile",
      component: () => import("../views/EditProfile.vue"),
    },

  ],
})
export default router
