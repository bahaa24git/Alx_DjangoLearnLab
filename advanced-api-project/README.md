## DRF Generic Views for Books

### Endpoints
- `GET /api/books/` — public list (filters: `?year=`, `?author=`, `?q=`; ordering: `?ordering=publication_year|-publication_year|title|-title`)
- `GET /api/books/<pk>/` — public detail
- `POST /api/books/create/` — **auth required**, create a book
- `PUT/PATCH /api/books/<pk>/update/` — **auth required**, update a book
- `DELETE /api/books/<pk>/delete/` — **auth required**, delete a book

### Permissions
- Read-only endpoints: `AllowAny`
- Write endpoints: `IsAuthenticated`
- (Optional) Global DRF settings enable Basic & Session Authentication for testing.

### Custom Behavior
- Create/Update accept **JSON** and **form-data** (via `JSONParser`, `FormParser`, `MultiPartParser`).
- Simple filters and ordering added in `BookListView.get_queryset`.
- Light server-side sanitation (strip title) in `perform_create/perform_update`.
- Validation for `publication_year` (no future years) in `BookSerializer`.

### Testing
Use Postman or `curl` (Basic Auth) to verify:
- Public GETs succeed without auth.
- POST/PUT/PATCH/DELETE are blocked without auth and succeed with valid credentials.

### Filtering, Searching, Ordering (DRF + django-filter)

- **Filtering (django-filter)** on `title`, `publication_year`, `author`, `author__name`.
  - Examples:
    - `/api/books/?title__icontains=war`
    - `/api/books/?publication_year__gte=1930&publication_year__lte=1950`
    - `/api/books/?author=1`
    - `/api/books/?author__name__icontains=orwell`
- **Search (SearchFilter)** across: `title`, `author__name`
  - Example: `/api/books/?search=farm`
  - Backward-compat: `/api/books/?q=farm` still works.
- **Ordering (OrderingFilter)** by `title`, `publication_year`, `id`
  - Example: `/api/books/?ordering=-publication_year,title`
