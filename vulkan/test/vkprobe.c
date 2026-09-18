#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vulkan/vulkan.h>

int main(void) {
    uint32_t count = 0;
    VkResult r;

    printf("OPENMIND VULKAN LOADER PROBE\n");
    printf("============================\n");

    r = vkEnumerateInstanceVersion(&count);
    if (r != VK_SUCCESS) {
        printf("vkEnumerateInstanceVersion failed: %d\n", r);
        return 1;
    }

    printf("Loader/API version: %u.%u.%u\n",
           VK_VERSION_MAJOR(count),
           VK_VERSION_MINOR(count),
           VK_VERSION_PATCH(count));

    VkApplicationInfo app = {
        .sType = VK_STRUCTURE_TYPE_APPLICATION_INFO,
        .pNext = NULL,
        .pApplicationName = "OpenMind",
        .applicationVersion = VK_MAKE_VERSION(1,0,0),
        .pEngineName = "OpenMind",
        .engineVersion = VK_MAKE_VERSION(1,0,0),
        .apiVersion = VK_MAKE_VERSION(1,0,0)
    };

    VkInstanceCreateInfo ci = {
        .sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
        .pNext = NULL,
        .flags = 0,
        .pApplicationInfo = &app,
        .enabledLayerCount = 0,
        .ppEnabledLayerNames = NULL,
        .enabledExtensionCount = 0,
        .ppEnabledExtensionNames = NULL
    };

    VkInstance instance = VK_NULL_HANDLE;

    r = vkCreateInstance(&ci, NULL, &instance);

    if (r != VK_SUCCESS) {
        printf("vkCreateInstance failed: %d\n", r);
        return 2;
    }

    printf("Vulkan instance: OK\n\n");

    uint32_t n = 0;
    r = vkEnumeratePhysicalDevices(instance, &n, NULL);

    if (r != VK_SUCCESS || n == 0) {
        printf("No Vulkan physical devices found.\n");
        printf("Result: %d, device count: %u\n", r, n);
        vkDestroyInstance(instance, NULL);
        return 3;
    }

    printf("Physical devices: %u\n\n", n);

    VkPhysicalDevice *devices =
        calloc(n, sizeof(VkPhysicalDevice));

    vkEnumeratePhysicalDevices(instance, &n, devices);

    for (uint32_t i = 0; i < n; i++) {
        VkPhysicalDeviceProperties p;

        vkGetPhysicalDeviceProperties(devices[i], &p);

        printf("GPU %u\n", i);
        printf("  Name       : %s\n", p.deviceName);
        printf("  Vendor     : 0x%04x\n", p.vendorID);
        printf("  Device     : 0x%04x\n", p.deviceID);
        printf("  Driver     : %u.%u.%u\n",
               VK_VERSION_MAJOR(p.driverVersion),
               VK_VERSION_MINOR(p.driverVersion),
               VK_VERSION_PATCH(p.driverVersion));
        printf("  API        : %u.%u.%u\n",
               VK_VERSION_MAJOR(p.apiVersion),
               VK_VERSION_MINOR(p.apiVersion),
               VK_VERSION_PATCH(p.apiVersion));
        printf("  Type       : %d\n", p.deviceType);
        printf("\n");
    }

    free(devices);
    vkDestroyInstance(instance, NULL);

    printf("VULKAN GPU PROBE: SUCCESS\n");

    return 0;
}
