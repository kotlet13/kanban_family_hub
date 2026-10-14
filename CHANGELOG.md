# Changelog

## 0.14.0 — 2026-10-14

- Add reviewed whole-space and project deletion with counted previews, durable tombstones, idempotent retries and post-commit private-image cleanup. Preserve accounts, devices, parents and unrelated financial facts; reject deletion graphs with external dependencies.
- Extend archival to household and organization spaces, including descendant write, invitation and delivery guards. Normal member removal revokes direct descendant access; child ownership requires resolution first.
- Add sync6/record6 for archived projects, idea-board format2 text sizing and garden-scene format3. Keep original queued operation identities and require compatible clients for richer records.
- Add task-relative reminders and negotiated push display format2. Modern Android renders grouped topic notifications; legacy Android and iOS retain operating-system alerts. Shopping notifications open the authorized parent list, including deleted-item context.
- Migrate schema17 to18 additively: scope deletion markers and private-file cleanup queue, relative-reminder fields and push notification-format registration. Existing registrations default to legacy format1.

Back up the database, private data tree and configuration before upgrading, and verify restoration. Source publication does not establish a hosted deployment or physical-device delivery.

## 0.13.0 — first standalone public source publication, 2026-10-13

- Editable idea-board records (`sync5`) with authenticated private photographs
  and image-attached annotations; complete board/image evidence for reports.
- Shared-content policy acceptance and content/member reporting, with private
  administrator review and bounded evidence retention.
- Whole-household/organization and project-only sharing, private synchronization,
  scoped finances and linked payments, invitations, account recovery/deletion.
- Existing bounded notification/reminder/email/push workers and read retention.

Schema17; PHP runtime source unchanged from the reviewed FamilyHub0.13.0 source
distribution. Source is published with a fresh history, installation ZIP,
MIT license and standalone documentation. This is not a new Jivie Android build
or an automatic upgrade of anyone's Kanboard installation.
